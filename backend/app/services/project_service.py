from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.models.project import Project
from app.models.user import User
from app.services.dashboard_service import file_path_to_url
from app.services.prediction_service import get_prediction_by_id


def list_projects(db: Session, user: User) -> list[dict]:
    projects = db.query(Project).filter(Project.user_id == user.id).order_by(Project.updated_at.desc()).all()
    result = []
    for project in projects:
        latest_image = (
            db.query(Prediction)
            .filter(Prediction.project_id == project.id, Prediction.user_id == user.id)
            .order_by(Prediction.updated_at.desc(), Prediction.created_at.desc())
            .first()
        )
        image_count = db.query(Prediction).filter(Prediction.project_id == project.id, Prediction.user_id == user.id).count()
        result.append(
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "image_count": image_count,
                "latest_thumbnail_url": file_path_to_url(latest_image.thumbnail_path if latest_image else None),
                "updated_at": project.updated_at.isoformat(),
                "status": project.status,
            }
        )
    return result


def create_project(db: Session, user: User, name: str, description: str | None = None, category: str | None = None) -> dict:
    project = Project(user_id=user.id, name=name, description=description, category=category)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description, "category": project.category, "status": project.status}


def update_project(db: Session, user: User, project_id: int, payload: dict) -> dict:
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field in ("name", "description", "category", "status"):
        if field in payload and payload[field] is not None:
            setattr(project, field, payload[field])
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description, "status": project.status}


def archive_project(db: Session, user: User, project_id: int) -> dict:
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.status = "archived"
    db.commit()
    return {"message": "Project archived"}


def add_image_to_project(db: Session, user: User, project_id: int, image_id: int) -> dict:
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    prediction = get_prediction_by_id(db, image_id, user.id)
    prediction.project_id = project.id
    if project.cover_image_id is None:
        project.cover_image_id = prediction.id
    db.commit()
    return {"message": "Image added to project"}


def get_project_images(db: Session, user: User, project_id: int) -> dict:
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    images = db.query(Prediction).filter(Prediction.project_id == project.id, Prediction.user_id == user.id).order_by(Prediction.updated_at.desc()).all()
    return {
        "project_id": project.id,
        "images": [
            {
                "id": image.id,
                "filename": image.original_filename,
                "original_url": file_path_to_url(image.original_image_path),
                "processed_url": file_path_to_url(image.output_image_path),
                "status": image.status,
            }
            for image in images
        ],
    }
