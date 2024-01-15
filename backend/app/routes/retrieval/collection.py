from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.services.retrieval.collection import *
from app.schemas.retrieval.collection import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse, BaseListRequest
from common.models import Collection, SerializePurpose

router = APIRouter()


@router.get(
    "/collections",
    tags=["Retrieval"],
    summary="List Collections",
    operation_id="list_collections",
    response_model=BaseSuccessListResponse,
)
async def api_list_collections(
    request: Request,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    collections, total, has_more = await list_collections(
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
    )
    return BaseSuccessListResponse(
        data=[collection.to_dict(purpose=SerializePurpose.RESPONSE) for collection in collections],
        fetched_count=len(collections),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/collections/{collection_id}",
    tags=["Retrieval"],
    summary="Get Collection",
    operation_id="get_collection",
    response_model=BaseSuccessDataResponse,
)
async def api_get_collection(
    collection_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    collection: Collection = await get_collection(
        collection_id=collection_id,
    )
    return BaseSuccessDataResponse(data=collection.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/collections",
    tags=["Retrieval"],
    summary="Bulk create collection",
    operation_id="bulk_create_collection",
    response_model=BaseSuccessDataResponse,
)
async def api_create_collections(
    request: Request,
    data: CollectionCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    collection: Collection = await create_collection(
        name=data.name,
        description=data.description,
        capacity=data.capacity,
        embedding_model_id=data.embedding_model_id,
        text_splitter=data.text_splitter,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(
        data=collection.to_dict(
            purpose=SerializePurpose.RESPONSE,
        )
    )


@router.post(
    "/collections/{collection_id}",
    tags=["Retrieval"],
    summary="Update Collection",
    operation_id="update_collection",
    response_model=BaseSuccessDataResponse,
)
async def api_update_collection(
    collection_id: str,
    request: Request,
    data: CollectionUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    collection: Collection = await update_collection(
        collection_id=collection_id,
        name=data.name,
        description=data.description,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=collection.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/collections/{collection_id}",
    tags=["Retrieval"],
    summary="Delete Collection",
    operation_id="delete_collection",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_collection(
    collection_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_collection(
        collection_id=collection_id,
    )
    return BaseSuccessEmptyResponse()
