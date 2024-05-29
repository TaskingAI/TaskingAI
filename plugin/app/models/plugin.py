from pydantic import BaseModel, Field
from typing import Dict, Any
from app.utils import i18n_text
from enum import Enum

__all__ = ["Plugin"]


class ParameterType(str, Enum):
    STRING = "string"  # str
    INTEGER = "integer"  # int
    NUMBER = "number"  # float
    BOOLEAN = "boolean"  # bool
    # OBJECT = "object" # dict, only for output
    # ARRAY = "array" # list, only for output
    STRING_ARRAY = "string_array"  # list of str
    INTEGER_ARRAY = "integer_array"  # list of int
    NUMBER_ARRAY = "number_array"  # list of float
    BOOLEAN_ARRAY = "boolean_array"  # list of bool
    IMAGE_URL = "image_url"  # str
    FILE_URL = "file_url"  # str


class ParameterSchema(BaseModel):
    type: ParameterType
    name: str
    description: str
    required: bool = Field(False)


class Plugin(BaseModel):
    bundle_id: str
    plugin_id: str
    name: str
    description: str
    input_schema: Dict[str, ParameterSchema]
    output_schema: Dict[str, ParameterSchema]

    @staticmethod
    def object_name():
        return "Plugin"

    @classmethod
    def build(cls, bundle_id: str, plugin_data: Dict):
        return cls(
            bundle_id=bundle_id,
            plugin_id=plugin_data["id"],
            name=plugin_data["name"] or "",
            description=plugin_data["description"],
            input_schema=plugin_data["input_schema"],
            output_schema=plugin_data["output_schema"],
        )

    def to_dict(self, lang: str):
        input_schema_dict = {
            k: {
                "type": v.type,
                "name": i18n_text(self.bundle_id, v.name, lang),
                "description": i18n_text(self.bundle_id, v.description, lang),
                "required": v.required,
            }
            for k, v in self.input_schema.items()
        }

        output_schema_dict = {
            k: {
                "type": v.type,
                "name": i18n_text(self.bundle_id, v.name, lang),
                "description": i18n_text(self.bundle_id, v.description, lang),
                "required": v.required,
            }
            for k, v in self.output_schema.items()
        }

        return {
            "object": self.object_name(),
            "bundle_id": self.bundle_id,
            "plugin_id": self.plugin_id,
            "name": i18n_text(self.bundle_id, self.name, lang),
            "description": i18n_text(self.bundle_id, self.description, lang),
            "input_schema": input_schema_dict,
            "output_schema": output_schema_dict,
        }

    def validate_input(self, input_params: Dict[str, Any]):
        # Iterate over the input_schema to validate each parameter
        for key, schema in self.input_schema.items():
            # Check if the parameter is required but missing
            if schema.required and key not in input_params:
                raise ValueError(f"'{key}' is required but not provided.")

            # If the parameter is present, perform type validation
            if key in input_params:
                value = input_params[key]

                if value is None:
                    continue
                # Validate based on the parameter's declared type
                if schema.type == ParameterType.STRING:
                    if not isinstance(value, str):
                        raise ValueError(f"Expected '{key}' to be a string, got {type(value).__name__}.")
                elif schema.type == ParameterType.INTEGER:
                    if not isinstance(value, int):
                        raise ValueError(f"Expected '{key}' to be an integer, got {type(value).__name__}.")
                elif schema.type == ParameterType.NUMBER:
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"Expected '{key}' to be a number, got {type(value).__name__}.")
                elif schema.type == ParameterType.BOOLEAN:
                    if not isinstance(value, bool):
                        raise ValueError(f"Expected '{key}' to be a boolean, got {type(value).__name__}.")
                elif schema.type == ParameterType.IMAGE_URL:
                    if not isinstance(value, str) or not value.startswith("http"):
                        raise ValueError(f"Expected '{key}' to be a valid image URL, got {type(value).__name__}.")
                elif schema.type == ParameterType.FILE_URL:
                    if not isinstance(value, str) or not value.startswith("http"):
                        raise ValueError(f"Expected '{key}' to be a valid file URL, got {type(value).__name__}.")
                elif schema.type == ParameterType.STRING_ARRAY:
                    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                        raise ValueError(f"Expected '{key}' to be a list of strings.")
                elif schema.type == ParameterType.INTEGER_ARRAY:
                    if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
                        raise ValueError(f"Expected '{key}' to be a list of integers.")
                elif schema.type == ParameterType.NUMBER_ARRAY:
                    if not isinstance(value, list) or not all(isinstance(item, (int, float)) for item in value):
                        raise ValueError(f"Expected '{key}' to be a list of numbers.")
                elif schema.type == ParameterType.BOOLEAN_ARRAY:
                    if not isinstance(value, list) or not all(isinstance(item, bool) for item in value):
                        raise ValueError(f"Expected '{key}' to be a list of booleans.")
                # Additional type checks can be added here for other types if necessary
