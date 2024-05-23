import yaml
from typing import Dict, Any
from app.error import raise_http_error, ErrorCode
from app.utils.i18n import collect_i18n_values, set_i18n
import os


def deep_merge_dicts(defaults: Dict[Any, Any], updates: Dict[Any, Any]) -> Dict[Any, Any]:
    result = defaults.copy()
    for key, value in updates.items():
        if isinstance(value, dict) and key in defaults and isinstance(defaults[key], dict):
            result[key] = deep_merge_dicts(defaults[key], value)
        else:
            result[key] = value
    return result


def load_config(config_schema: Dict) -> Dict:
    config_id = config_schema.get("config_id")
    file_path = os.path.join(os.path.dirname(__file__), f"./resources/configs/{config_id}.yml")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            config_str = file.read()
            config_dict = yaml.safe_load(config_str)
    else:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"No YAML file found for config_id {config_id}")

    merged_config = deep_merge_dicts(config_dict, config_schema)

    # read i18n files: en.yml, zh.yml, fr.yml, etc.
    i18n_keys = collect_i18n_values(config_str)
    i18n_dir_path = os.path.join(os.path.dirname(__file__), f"./resources/i18n")
    for i18n_file in os.listdir(i18n_dir_path):
        if i18n_file.endswith(".yml"):
            lang = i18n_file.split(".")[0]
            with open(os.path.join(i18n_dir_path, i18n_file), "r") as file:
                i18n_data = yaml.safe_load(file)
                # check if all keys are present
                for key in i18n_keys:
                    if key[5:] not in i18n_data:
                        config_name = merged_config.get("config_id", "unknown config")
                        raise_http_error(
                            ErrorCode.OBJECT_NOT_FOUND, f"{config_name}'s i18n key {key[5:]} is missing in {i18n_file}"
                        )
                set_i18n("config_schema", lang, i18n_data)

    return merged_config


def validate_config_value(value: Any, schema: Dict):
    if schema["type"] == "array":
        if not isinstance(value, list):
            return False
        if not (schema["min_items"] <= len(value) <= schema["max_items"]):
            return False
        for item in value:
            if not isinstance(item, str) or not (
                schema["items"]["min_length"] <= len(item) <= schema["items"]["max_length"]
            ):
                return False
    elif schema["type"] == "int":
        if not isinstance(value, int):
            return False
        if not (schema["min"] <= value <= schema["max"]):
            return False
    elif schema["type"] == "float":
        if not isinstance(value, float):
            return False
        if not (schema["min"] <= value <= schema["max"]):
            return False
    return True
