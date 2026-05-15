from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.project import ProjectAddImageRequest, ProjectCreateRequest, ProjectUpdateRequest
from app.services.project_service import add_image_to_project, archive_project, create_project, get_project_images, list_projects, update_project

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"projects": list_projects(db, current_user)}


@router.post("")
def create_new_project(payload: ProjectCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_project(db, current_user, payload.name, payload.description, payload.category)


@router.put("/{project_id}")
def edit_project(project_id: int, payload: ProjectUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_project(db, current_user, project_id, payload.model_dump(exclude_none=True))


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return archive_project(db, current_user, project_id)


@router.post("/{project_id}/add-image")
def attach_image_to_project(project_id: int, payload: ProjectAddImageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_image_to_project(db, current_user, project_id, payload.image_id)


@router.get("/{project_id}/images")
def project_images(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_images(db, current_user, project_id)
