from pydantic import BaseModel


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    status: str | None = None


class ProjectAddImageRequest(BaseModel):
    image_id: int
