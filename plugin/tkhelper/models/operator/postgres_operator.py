from typing import Optional, Dict, List, Type
from asyncpg.exceptions import UniqueViolationError

from tkhelper.database.postgres import PostgresDatabasePool
from tkhelper.database.postgres import ops as postgres_ops
from tkhelper.error import raise_http_error, ErrorCode

from ..type import SortOrderEnum
from ..entity import ModelEntity
from .operator import ModelOperator
from ..redis import RedisOperator

__all__ = ["PostgresModelOperator"]


class PostgresModelOperator(ModelOperator):
    def __init__(
        self,
        postgres_pool: PostgresDatabasePool,
        entity_class: Type[ModelEntity],
        redis: RedisOperator = None,
    ):
        self.postgres_pool = postgres_pool
        super().__init__(entity_class, redis)

    # --- db methods ---

    async def _update_entity(self, conn, entity: ModelEntity, update_dict: Dict) -> ModelEntity:
        if self.redis:
            await self.redis.pop(entity)
        await postgres_ops.update_object(
            conn=conn,
            table_name=self.entity_class.table_name(),
            equal_filters={k: getattr(entity, k) for k in self.entity_class.primary_key_fields()},
            update_dict=update_dict,
        )
        entity = await self.get(
            **{k: getattr(entity, k) for k in self.entity_class.primary_key_fields()},
            postgres_conn=conn,
        )
        return entity

    async def update_entity(self, entity: ModelEntity, update_dict: Dict, **kwargs) -> ModelEntity:
        conn = kwargs.pop("postgres_conn", None)
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                return await self._update_entity(conn, entity, update_dict)
        else:
            return await self._update_entity(conn, entity, update_dict)

    async def update(self, update_dict: Dict, **kwargs) -> ModelEntity:
        conn = kwargs.pop("postgres_conn", None)
        entity = await self.get(**kwargs, postgres_conn=conn)
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                return await self._update_entity(conn, entity, update_dict)
        else:
            return await self._update_entity(conn, entity, update_dict)

    async def _delete_entity(self, conn, entity: ModelEntity) -> None:
        if self.redis:
            await self.redis.pop(entity)

        await postgres_ops.delete_object(
            conn=conn,
            table_name=self.entity_class.table_name(),
            equal_filters={k: getattr(entity, k) for k in self.entity_class.primary_key_fields()},
        )

    async def delete_entity(self, entity: ModelEntity, **kwargs) -> None:
        conn = kwargs.pop("postgres_conn", None)
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                await self._delete_entity(conn, entity)
        else:
            await self._delete_entity(conn, entity)

    async def delete(self, **kwargs) -> None:
        conn = kwargs.pop("postgres_conn", None)
        entity = await self.get(**kwargs, postgres_conn=conn)
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                await self._delete_entity(conn, entity)
        else:
            await self._delete_entity(conn, entity)

    async def _get_entity(self, conn, **kwargs) -> Optional[ModelEntity]:
        object_dict = await postgres_ops.get_object(
            conn=conn,
            table_name=self.entity_class.table_name(),
            equal_filters={k: v for k, v in kwargs.items() if k in self.entity_class.primary_key_fields()},
        )
        return self.entity_class.build(object_dict) if object_dict else None

    async def get(self, raise_not_found_error=True, **kwargs) -> Optional[ModelEntity]:
        # check kwargs contains all the primary key fields
        kwargs = self._check_kwargs(object_id_required=True, **kwargs)
        conn = kwargs.pop("postgres_conn", None)

        # get from redis
        if self.redis:
            entity = await self.redis.get(**kwargs)
            if entity:
                return entity

        # get from postgres
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                entity = await self._get_entity(conn, **kwargs)
        else:
            entity = await self._get_entity(conn, **kwargs)

        if entity:
            return entity
        elif raise_not_found_error:
            object_id = kwargs.get(self.entity_class.id_field_name())
            raise_http_error(
                ErrorCode.OBJECT_NOT_FOUND,
                f"{self.entity_class.object_name()} {object_id} not found",
            )

        return None

    async def _create_entity(self, conn, create_dict: Dict, **kwargs) -> ModelEntity:
        # add kwargs to create_dict
        create_dict.update(kwargs)
        object_id = create_dict.get(self.entity_class.id_field_name())
        if not object_id:
            # create new id if not provided
            object_id = self.entity_class.generate_random_id()
            create_dict[self.entity_class.id_field_name()] = object_id

        try:
            await postgres_ops.create_object(
                conn,
                table_name=self.entity_class.table_name(),
                object_dict=create_dict,
                primary_keys=self.entity_class.primary_key_fields(),
            )
        except UniqueViolationError as e:
            raise_http_error(
                ErrorCode.DUPLICATE_OBJECT,
                f"The {self.entity_class.object_name()} {object_id} already exists.",
            )

        pk_dict = {k: create_dict[k] for k in self.entity_class.primary_key_fields()}
        entity = await self.get(postgres_conn=conn, **pk_dict)
        return entity

    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # check kwargs contains all the primary key fields except the id field
        kwargs = self._check_kwargs(object_id_required=None, **kwargs)
        conn = kwargs.pop("postgres_conn", None)

        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                async with conn.transaction():
                    return await self._create_entity(conn, create_dict, **kwargs)
        else:
            return await self._create_entity(conn, create_dict, **kwargs)

    async def _bulk_create_entities(self, conn, create_dict_list: List[Dict], **kwargs) -> List[ModelEntity]:
        for create_dict in create_dict_list:
            # create object
            create_dict.update(kwargs)
            object_id = create_dict.get(self.entity_class.id_field_name())
            if not object_id:
                # create new id if not provided
                object_id = self.entity_class.generate_random_id()
                create_dict[self.entity_class.id_field_name()] = object_id

            try:
                await postgres_ops.create_object(
                    conn,
                    table_name=self.entity_class.table_name(),
                    object_dict=create_dict,
                    primary_keys=self.entity_class.primary_key_fields(),
                )
            except UniqueViolationError as e:
                raise_http_error(
                    ErrorCode.DUPLICATE_OBJECT,
                    f"The {self.entity_class.object_name()} {create_dict[self.entity_class.id_field_name()]} already exists.",
                )

        entities = []
        for create_dict in create_dict_list:
            pk_dict = {k: create_dict[k] for k in self.entity_class.primary_key_fields()}
            entity = await self.get(**pk_dict, postgres_conn=conn)
            entities.append(entity)

        return entities

    async def bulk_create(
        self,
        create_dict_list: List[Dict],
        **kwargs,
    ) -> List[ModelEntity]:
        # check kwargs contains all the primary key fields except the id field
        kwargs = self._check_kwargs(object_id_required=False, **kwargs)
        conn = kwargs.pop("postgres_conn", None)

        # add new id and add kwargs to create_dict
        if not conn:
            async with self.postgres_pool.get_db_connection() as conn:
                async with conn.transaction():
                    return await self._bulk_create_entities(conn, create_dict_list, **kwargs)
        else:
            return await self._bulk_create_entities(conn, create_dict_list, **kwargs)

    async def list(
        self,
        limit: int,
        order: SortOrderEnum,
        after_id: Optional[str] = None,
        before_id: Optional[str] = None,
        prefix_filters: Optional[Dict] = None,
        equal_filters: Optional[Dict] = None,
        **kwargs,
    ) -> (List[ModelEntity], bool):
        # check kwargs contains all the primary key fields except the id field
        kwargs = self._check_kwargs(object_id_required=False, **kwargs)

        # use kwargs + self.id_field_name(): after_id to get after_object

        after = None
        if after_id:
            after_kwargs = {**kwargs, self.entity_class.id_field_name(): after_id}
            after = await self.get(**after_kwargs)

        before = None
        if before_id:
            before_kwargs = {**kwargs, self.entity_class.id_field_name(): before_id}
            before = await self.get(**before_kwargs)

        # update equal_filters with kwargs
        if not equal_filters:
            equal_filters = {}
        equal_filters.update({k: v for k, v in kwargs.items()})

        async with self.postgres_pool.get_db_connection() as conn:
            object_dicts, has_more = await postgres_ops.list_objects(
                conn=conn,
                table_name=self.entity_class.table_name(),
                order=order,
                sort_field="created_timestamp",  # TODO: make this configurable
                object_id_name=self.entity_class.id_field_name(),
                limit=limit,
                after_id=getattr(after, self.entity_class.id_field_name()) if after else None,
                after_value=getattr(after, "created_timestamp") if after else None,
                before_id=getattr(before, self.entity_class.id_field_name()) if before else None,
                before_value=getattr(before, "created_timestamp") if before else None,
                offset=None,
                prefix_filters=prefix_filters,
                equal_filters=equal_filters,
            )
            entities = [self.entity_class.build(object_dict) for object_dict in object_dicts]
            return entities, has_more
