from abc import ABC, abstractmethod
from pydantic import BaseModel, create_model
from typing import Dict, List
import copy

entity_path_param_validator: Dict[str, BaseModel] = {}


class ModelEntity(BaseModel, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    @abstractmethod
    def build(row: Dict):
        raise NotImplementedError

    # -- serialization --

    def to_redis_dict(self) -> Dict:
        return self.model_dump()

    def to_response_dict(self) -> Dict:
        response_dict = self.model_dump()
        for field in self.fields_exclude_in_response():
            response_dict.pop(field, None)
        return response_dict

    # --- static attributes ---

    @staticmethod
    @abstractmethod
    def object_name() -> str:
        raise NotImplementedError

    @classmethod
    def object_capitalized_name(cls) -> str:
        # if name has _ then capitalize each word
        if "_" in cls.object_name():
            return " ".join([x.capitalize() for x in cls.object_name().split("_")])
        return cls.object_name().capitalize()

    @staticmethod
    @abstractmethod
    def object_plural_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def id_field_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def primary_key_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def path_params_to_primary_key_params(path_params: Dict) -> Dict:
        return path_params

    @classmethod
    def object_capitalized_plural_name(cls) -> str:
        # if name has _ then capitalize each word
        if "_" in cls.object_plural_name():
            return " ".join([x.capitalize() for x in cls.object_plural_name().split("_")])
        return cls.object_plural_name().capitalize()

    @staticmethod
    @abstractmethod
    def table_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_random_id(**kwargs) -> str:
        raise NotImplementedError

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return []

    @staticmethod
    def list_equal_filter_fields() -> List[str]:
        return []

    @staticmethod
    @abstractmethod
    def parent_models() -> List:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parent_operator() -> List:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_fields() -> List[str]:
        """
        fields to be used for create.
        if "max_count" is in the list, it will be used for the count check when creating.
        if "object_id" is in the list, it will be used for create the object id.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def fields_exclude_in_response():
        raise NotImplementedError

    @classmethod
    def validate_path_params(cls, path_params: Dict):
        global entity_path_param_validator

        k = ":".join(sorted(list(path_params.keys())))
        validator = entity_path_param_validator.get(k)

        if validator is not None:
            validator.validate(path_params)

        else:
            # create a path param validator
            fields = {}
            for field_name in path_params:
                field = cls.model_fields.get(field_name)
                if field:
                    field_copy = copy.copy(field)
                    fields[field_name] = (field.annotation, field_copy)
            validator = create_model(
                f"{cls.object_name()}PathParamValidator",
                **fields,
            )
            validator.validate(path_params)
            entity_path_param_validator[k] = validator
