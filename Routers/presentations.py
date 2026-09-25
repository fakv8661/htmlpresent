import os

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse, JSONResponse

from templates_config import templates, templates_present
from Database import database
import utils

router = APIRouter(tags=['presentations'])

@router.get("/presentation")
async def prsentationpg(request: Request):
    # LEGACY!!!
    # убрать после рекода фронтенда
    presentations = utils.get_presentationlist(await database.PresentationDatabase.GetAllPresentations(), request)
    # вот это
    return templates.TemplateResponse(
        request,
        "presentation_page.html",
        context={"presentations": presentations},
    )

@router.get("/presentation/{present_id}")
async def presentationgt(present_id: int, request: Request):
    present = await database.PresentationDatabase.GetPresentationByID(present_id)
    if present is None:
        return RedirectResponse(url="/")
    if os.path.exists(os.path.join("templates/presentations", present.file)):
        if "html" in present.file.split("."):
            return templates_present.TemplateResponse(request, present.file)
        else:
            return FileResponse(
            path=f"templates/presentations/{present.file}",
            filename=f"presentation_{id}.pdf",
            headers={"Content-Disposition": "inline"}
        )

    else:
        return RedirectResponse(url="/")

@router.get("/presentations")
async def presentationlst(request: Request):
    presentations = utils.get_presentationlist(await database.PresentationDatabase.GetAllPresentations(), request)

    return JSONResponse(presentations)