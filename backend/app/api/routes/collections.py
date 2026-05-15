from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.collections_service import (
    add_collection_item_payload,
    create_collection_payload,
    get_collection_detail_payload,
    list_collections_payload,
    remove_collection_item_payload,
)

router = APIRouter(prefix="/api/collections", tags=["collections"])


class CreateCollectionRequest(BaseModel):
    name: str


class AddCollectionItemRequest(BaseModel):
    prediction_id: int


@router.get("")
def get_collections(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_collections_payload(db, current_user)


@router.post("")
def create_collection(payload: CreateCollectionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_collection_payload(db, current_user, payload.name)


@router.post("/{collection_id}/items")
def add_collection_item(
    collection_id: int,
    payload: AddCollectionItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_collection_item_payload(db, current_user, collection_id, payload.prediction_id)


@router.get("/{collection_id}")
def get_collection_detail(collection_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_collection_detail_payload(db, current_user, collection_id)


@router.delete("/{collection_id}/items/{prediction_id}")
def remove_collection_item(
    collection_id: int,
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_collection_item_payload(db, current_user, collection_id, prediction_id)
