from pydantic import BaseModel, Field
from typing import Any, Dict
from enum import Enum
from app.models import ChatCompletionFunction

__all__ = ["Plugin"]


class ParameterType(str, Enum):
    STRING = "string"  # str
    INTEGER = "integer"  # int
    NUMBER = "number"  # float
    BOOLEAN = "boolean"  # bool
    OBJECT = "object"  # dict, only for output
    ARRAY = "array"  # list, only for output
    IMAGE_URL = "image_url"  # str
    FILE_URL = "file_url"  # str


class ParameterSchema(BaseModel):
    type: ParameterType
    name: str
    description: str
    required: bool = Field(False)


def transform_input_schema(bundle_id, plugin_id, plugin_description, input_schema: Dict) -> ChatCompletionFunction:
    """
    Transforms the input schema into the specified output format,
    retaining only 'type', 'enum', and 'description' fields in the final dict.
    """
    from app.services.tool import i18n_text

    # Initialize the base structure of the output schema
    output_schema = {
        "name": "object",
        "properties": {},
        "required": [],
    }

    for key, value in input_schema.items():
        # Copy only 'type', 'enum', and 'description' fields to the new schema
        filtered_value = {k: v for k, v in value.items() if k in ["type", "enum", "description"]}
        output_schema["properties"][key] = filtered_value

        if filtered_value.get("description"):
            # handle i18n
            output_schema["properties"][key]["description"] = i18n_text(bundle_id, value["description"], "en")

        # If the original field is required, add it to the 'required' list in the output schema
        if value.get("required"):
            output_schema["required"].append(key)

    function = ChatCompletionFunction(
        name=plugin_id,
        description=i18n_text(bundle_id, plugin_description, "en"),
        parameters=output_schema,
    )
    return function


class Plugin(BaseModel):
    bundle_id: str
    plugin_id: str
    name: str
    description: str
    input_schema: Dict[str, ParameterSchema]
    output_schema: Dict[str, ParameterSchema]
    function_def: ChatCompletionFunction = Field(exclude=True)

    @staticmethod
    def object_name():
        return "Plugin"

    @classmethod
    def build(cls, data: Dict):
        function_def = transform_input_schema(
            data["bundle_id"],
            data["plugin_id"],
            data["description"],
            data["input_schema"],
        )
        return cls(
            bundle_id=data["bundle_id"],
            plugin_id=data["plugin_id"],
            name=data["name"] or "",
            description=data["description"],
            input_schema=data["input_schema"],
            output_schema=data["output_schema"],
            function_def=function_def,
        )

    def to_dict(self, lang: str):
        from app.services.tool import i18n_text

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
            "function_def": self.function_def,
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
                # Additional type checks can be added here for other types if necessary
