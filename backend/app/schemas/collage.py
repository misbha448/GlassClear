from pydantic import BaseModel, Field


class CollageImageInput(BaseModel):
    image_id: int | None = None
    url: str | None = None
    label: str | None = None


class CollageCreateRequest(BaseModel):
    layout_type: str
    image_ids: list[int] = Field(default_factory=list)
    images: list[CollageImageInput] = Field(default_factory=list)
    title: str = "GlassClear Collage"
