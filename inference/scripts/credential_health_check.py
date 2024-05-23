import os
from test.utils.utils import get_yaml_files, load_yaml, white_list_models
import asyncio
import json
from app.models import (
    ChatCompletionModelConfiguration,
    ChatCompletionUserMessage,
    TextEmbeddingModelConfiguration,
    TextEmbeddingModelProperties,
    validate_credentials,
    validate_model_info,
)
from app.cache import load_provider_data, load_model_schema_data

provider_ids = load_provider_data()
load_model_schema_data(provider_ids)


def generate_test_cases():
    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../providers")
    cases = []
    for provider_id in provider_ids:
        provider_path = os.path.join(providers_path, provider_id, "resources")
        provider_yaml_data = load_yaml(os.path.join(provider_path, "provider.yml"))

        credentials_schema = provider_yaml_data["credentials_schema"]
        credential_set = []
        index = 0
        while True:
            credentials = {}
            for key in credentials_schema["required"]:
                env_key = key if index == 0 else f"{key}_{index}"
                credentials[key] = os.environ.get(env_key)

            if not any(credentials.values()):
                break
            credentials["index"] = index
            index += 1
            credential_set.append(credentials)
        if not credential_set:
            continue

        models_path = os.path.join(providers_path, provider_id, "resources/models")
        yaml_files = get_yaml_files(models_path)

        yaml_data = None
        for yaml_file in yaml_files:
            file_path = os.path.join(models_path, yaml_file)
            yaml_data = load_yaml(file_path)
            if yaml_data["model_schema_id"] not in white_list_models and yaml_file != "wildcard.yml":
                break
        if not yaml_data or yaml_data["type"] == "wildcard":
            continue

        for credential in credential_set:
            base_test_case = {
                "model_schema_id": yaml_data["model_schema_id"],
                "provider_id": provider_id,
                "provider_model_id": yaml_data["provider_model_id"],
                "model_type": yaml_data["type"],
                "credentials": credential,
                "properties": yaml_data.get("properties", {}),
            }
            cases.append(base_test_case)

    return cases


async def test_credential_health_check(test_data):
    model_schema_id = test_data["model_schema_id"]
    provider_model_id = test_data["provider_model_id"]
    provider_id = test_data["provider_id"]
    model_type = test_data["model_type"]
    credentials = test_data["credentials"]
    properties = test_data["properties"]
    test_result = {"provider": provider_id, "status": "fail", "index": credentials.get("index")}
    attempts = 0
    max_attempts = 2
    success = False
    while attempts < max_attempts and not success:
        try:
            model_infos = [
                validate_model_info(
                    model_schema_id=model_schema_id,
                    provider_model_id=provider_model_id,
                    properties_dict=None,
                    model_type=model_type,
                )
            ]

            provider_credentials = validate_credentials(
                model_infos=model_infos,
                credentials_dict=credentials,
                encrypted_credentials_dict={},
            )

            if model_type == "chat_completion":
                from app.routes.chat_completion.route import chat_completion

                message = ChatCompletionUserMessage.model_validate({"role": "user", "content": "Hello!"})
                config = ChatCompletionModelConfiguration()
                setattr(config, "max_tokens", 3)

                response = await chat_completion(
                    model_infos=model_infos,
                    messages=[message],
                    credentials=provider_credentials,
                    configs=config,
                )
                result = response.model_dump()
                if result.get("message") is not None:
                    test_result["status"] = "success"
                    success = True
                else:
                    attempts += 1  # Increment attempts for a potential retry
                    if attempts == max_attempts:  # Check if this was the last attempt
                        test_result["error"] = "No data returned after retry"

            elif model_type == "text_embedding":
                from app.routes.text_embedding.route import embed_text

                real_properties = TextEmbeddingModelProperties(embedding_size=properties.get("embedding_size", 768))
                real_properties.max_batch_size = properties.get("max_batch_size", 512)
                response = await embed_text(
                    provider_id=provider_id,
                    provider_model_id=provider_model_id,
                    input=["Hello"],
                    credentials=provider_credentials,
                    properties=real_properties,
                    configs=TextEmbeddingModelConfiguration(),
                    input_type=None,
                )
                result = response.model_dump()
                if result.get("data"):
                    test_result["status"] = "success"
                    success = True
                else:
                    attempts += 1
                    if attempts == max_attempts:
                        test_result["error"] = "No data returned after retry"
            else:
                test_result["error"] = "Unsupported model type"
                break
        except Exception as e:
            attempts += 1
            if attempts == max_attempts:
                test_result["error"] = f"retry: {attempts}, detail: {str(e)}"

    return test_result


async def run_all_tests(cases):
    results = await asyncio.gather(*(test_credential_health_check(case) for case in cases))
    return results


def main():
    cases = generate_test_cases()

    results = asyncio.run(run_all_tests(cases))
    overall_status = "success"
    for result in results:
        if result["status"] == "fail":
            overall_status = "fail"
            break

    final_result = {"status": overall_status, "data": results}
    print(json.dumps(final_result, indent=2))


if __name__ == "__main__":
    main()
