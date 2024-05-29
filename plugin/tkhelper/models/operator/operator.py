from abc import abstractmethod, ABC
from typing import Optional, Dict, List, Type
from ..type import SortOrderEnum
from ..entity import ModelEntity
from ..redis import RedisOperator

__all__ = ["ModelOperator"]


class ModelOperator(ABC):
    def __init__(
        self,
        entity_class: Type[ModelEntity],
        redis: RedisOperator = None,
    ):
        self.entity_class = entity_class
        self.redis = redis

    # --- db methods ---

    @abstractmethod
    async def update(self, update_dict: Dict, **kwargs) -> ModelEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_entity(self, entity: ModelEntity, update_dict: Dict) -> ModelEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_entity(self, entity: ModelEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, raise_not_found_error=True, **kwargs) -> Optional[ModelEntity]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, create_dict: Dict, **kwargs) -> ModelEntity:
        raise NotImplementedError

    @abstractmethod
    async def bulk_create(self, create_dict_list: List[Dict], **kwargs) -> List[ModelEntity]:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        limit: int,
        order: SortOrderEnum,
        after_object: Optional[ModelEntity] = None,
        before_object: Optional[ModelEntity] = None,
        offset: int = 0,
        prefix_filters: Optional[Dict] = None,
        equal_filters: Optional[Dict] = None,
        **kwargs,
    ):
        raise NotImplementedError

    # -- helper methods

    def _check_kwargs(self, object_id_required: Optional[bool], **kwargs) -> Dict:
        """
        Check if kwargs contains all the primary key fields except the id field.

        :param object_id_required: if object_id is required
        :param kwargs: kwargs
        :return: the updated kwargs

        """

        if (
            (object_id_required is not None)
            and (not object_id_required)
            and (self.entity_class.id_field_name() in kwargs)
        ):
            raise ValueError("Object id should not be in kwargs")

        required_fields = [field for field in self.entity_class.primary_key_fields() if "id" in field]
        for k in required_fields:
            if k not in kwargs and (k != self.entity_class.id_field_name() or object_id_required):
                raise ValueError(f"Missing primary key field: {k}")

        # field all path_params in kwargs
        if object_id_required:
            path_params = {k: v for k, v in kwargs.items() if k in self.entity_class.primary_key_fields()}
            primary_key_params = self.entity_class.path_params_to_primary_key_params(path_params)
            kwargs.update(primary_key_params)

        return kwargs
