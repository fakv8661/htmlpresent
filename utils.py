import os

from fastapi.requests import Request

from Database import models


def get_presentationlist(presentations: list[models.Presentation], request: Request):
    presentationks = []

    for present in presentations:
        presentationks.append({
            "id": present.id,
            "title": present.name,
            "authors": present.author,
            "description": present.description,
            "cover": request.url_for("presentation_asset", path=os.path.join("preview_img/", present.preview_image))._url if present.preview_image else None
        })

    return presentationks