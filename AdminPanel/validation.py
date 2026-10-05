from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel
from pydantic import Field, field_validator
from pydantic import ValidationError, TypeAdapter

class PresentationAddSchema(BaseModel):
    name: str = Field(min_length=3, max_length=256)
    author: str = Field(min_length=3, max_length=256)
    description: str = Field(max_length=500)
    image: Path | None
    file: Path

    _images_type: ClassVar[frozenset[str]] = frozenset({
        ".jpg", ".jpeg", ".png", ".webp",
        ".gif", ".avif", ".svg", ".apng",
        ".bmp", ".ico"
    })

    @field_validator("image", mode='after')
    def image_validator(image: Path | None) -> Path | None:
        if image is None:
            return None
        if image.suffix.lower() not in PresentationAddSchema._images_type:
            raise ValidationError("Image not supported!")
        else:
            return image