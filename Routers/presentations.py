import os

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse, JSONResponse

from templates_config import templates, templates_present
from Database import database
import utils

router = APIRouter(tags=['presentations'])

@router.get("/pres/{present_id}")
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

@router.get("/pres")
async def presentationlst(request: Request):
    presentations = utils.get_presentationlist(await database.PresentationDatabase.GetAllPresentations(), request)

    return JSONResponse(presentations)