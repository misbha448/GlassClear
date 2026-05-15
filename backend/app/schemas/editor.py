from typing import Any

from pydantic import BaseModel


class ApplyReflectionRequest(BaseModel):
    image_id: int
    settings: dict[str, Any] | None = None


class ApplyToolRequest(BaseModel):
    image_id: int
    tool: str
    settings: dict[str, Any] | None = None


class SetCurrentImageRequest(BaseModel):
    image_id: int


class ExportRequest(BaseModel):
    image_id: int
    export_type: str | None = None
    type: str | None = None
