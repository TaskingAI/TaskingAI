import yaml
import os
from dotenv import load_dotenv

load_dotenv()


# Read all YAML files in the specified directory
def get_yaml_files(directory):
    yaml_files = [f for f in os.listdir(directory) if f.endswith(".yml") or f.endswith(".yaml")]
    return yaml_files


# Read a single YAML file
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def load_default_credentials(path):
    config = {}

    # Open and parse the .env file
    with open(path) as f:
        for line in f:
            # Strip whitespace and ignore comments
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key] = value

    return config


def generate_test_cases():

    bundles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../bundles")
    bundle_dir_names = [name for name in os.listdir(bundles_path) if os.path.isdir(os.path.join(bundles_path, name))]
    bundle_dir_names = [name for name in bundle_dir_names if not name.startswith("_")]

    cases = []
    for bundle_dir_name in bundle_dir_names:

        if bundle_dir_name in [
            "aftership",
            "coin_market_cap",
            "api_ninjas_commodity_price",
            "geospy_api",
            "weather_bit",
            "duckduckgo",
        ]:
            continue

        bundle_dir_path = os.path.join(bundles_path, bundle_dir_name)
        bundle_schema_path = os.path.join(bundle_dir_path, "resources/bundle_schema.yml")
        bundle_yaml_data = load_yaml(bundle_schema_path)

        bundle_id = bundle_dir_name
        bundle_credentials = [name for name in bundle_yaml_data.get("credentials_schema", {}).keys()]

        bundle_plugins_path = os.path.join(bundle_dir_path, "plugins")
        plugin_ids = [
            id for id in os.listdir(bundle_plugins_path) if os.path.isdir(os.path.join(bundle_plugins_path, id))
        ]
        plugin_ids = [id for id in plugin_ids if not id.startswith("_")]

        for plugin_id in plugin_ids:
            if plugin_id in ["get_historical_exchange_rate", "chat_completion_by_gemini_1_0_pro"]:
                continue
            plugin_path = os.path.join(bundle_plugins_path, plugin_id)
            plugin_schema_path = os.path.join(plugin_path, "plugin_schema.yml")
            plugin_yaml_data = load_yaml(plugin_schema_path)

            output_schema = plugin_yaml_data.get("output_schema", {})
            test_info = plugin_yaml_data.get("test", {})
            mode = test_info.get("mode", "schema")
            test_cases = test_info.get("cases", {})

            for test_case in test_cases:
                cases.append(
                    {
                        "id": f"{bundle_id}/{plugin_id}",
                        "bundle_id": bundle_id,
                        "bundle_credentials": bundle_credentials,
                        "plugin_id": plugin_id,
                        "output_schema": output_schema,
                        "mode": mode,
                        "input": test_case.get("input", {}),
                        "output": test_case.get("output", {}),
                    }
                )

    return cases


class ResponseWrapper:
    def __init__(self, status: int, json_data: dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data
