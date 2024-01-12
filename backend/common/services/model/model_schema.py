from typing import Optional, List
import os
from common.models import Provider, ModelSchema, ListResult
import yaml

__all__ = [
    "list_providers",
    "list_model_schemas",
]


def _load_data_from_files(directory_path):
    providers = []
    model_schemas = []

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Check if file is not empty
        if os.path.getsize(file_path) > 0:
            try:
                # Open and read the file
                with open(file_path, "r") as file:
                    data = yaml.safe_load(file)  # Use yaml.safe_load to load YAML data

                # Process the data
                provider_data = data["provider"]
                provider = Provider.build(provider_data)
                providers.append(provider)

                for model_schema_data in provider_data["model_schemas"]:
                    model_schema_data["provider_id"] = provider.provider_id
                    model_schema = ModelSchema.build(model_schema_data)
                    model_schemas.append(model_schema)

            except yaml.YAMLError as e:
                print(f"Error loading YAML from file {file_path}: {e}")
        else:
            print(f"Skipping empty file: {file_path}")

    # sort provider by name
    providers.sort(key=lambda x: x.name)

    # sort model schemas by provider_id, name
    model_schemas.sort(key=lambda x: (x.provider_id, x.name))

    return providers, model_schemas


_providers, _model_schemas = _load_data_from_files(
    os.path.dirname(os.path.realpath(__file__)) + "/../../../resources/data/model_schemas"
)


async def list_providers() -> List[Provider]:
    return _providers


async def list_model_schemas(
    limit: int,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    provider_id: Optional[str],
    type: Optional[str],
) -> ListResult:
    """
    List model schemas.
    Only one in `offset`, `after` and `before` can be used at the same time.

    :param limit: the maximum number of model schemas to return.
    :param after: the cursor represented by a model_schema_id to fetch the next page.
    :param before: the cursor represented by a model_schema_id to fetch the previous page.
    :param offset: the offset of model schemas to return.
    :param provider_id: the provider id to filter by.
    :param type: the model type to filter by.
    :return: a tuple of (model schemas, total count, has more)
    """

    # Ensure only one of after, before, or offset is used
    if sum(x is not None for x in [after, before, offset]) > 1:
        raise ValueError("Only one of 'after', 'before', or 'offset' can be used")

    # Filter by provider_id and type
    filtered_schemas = [
        schema
        for schema in _model_schemas
        if (provider_id is None or schema.provider_id == provider_id) and (type is None or schema.type == type)
    ]

    # Find the index for pagination
    start_index = 0
    if after:
        start_index = next(
            (i for i, schema in enumerate(filtered_schemas) if schema.model_schema_id == after), len(filtered_schemas)
        )
    elif before:
        start_index = (
            next((i for i, schema in enumerate(filtered_schemas) if schema.model_schema_id == before), 0) - limit
        )
        start_index = max(0, start_index)
    elif offset is not None:
        start_index = offset

    # Paginate
    end_index = start_index + limit
    page = filtered_schemas[start_index:end_index]

    # Check if there's more
    has_more = end_index < len(filtered_schemas)

    return page, len(filtered_schemas), has_more


def get_provider(provider_id: str) -> Optional[Provider]:
    """
    Get a provider by provider_id.

    :param provider_id: the provider id.
    :return: the provider or None if not found.
    """
    return next((provider for provider in _providers if provider.provider_id == provider_id), None)


def get_model_schema(model_schema_id: str) -> Optional[ModelSchema]:
    """
    Get a model schema by model_schema_id.

    :param model_schema_id: the model schema id.
    :return: the model schema or None if not found.
    """
    return next((schema for schema in _model_schemas if schema.model_schema_id == model_schema_id), None)
