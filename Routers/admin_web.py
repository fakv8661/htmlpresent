import os

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse, JSONResponse

from templates_config import templates, templates_present
from Database import database
import utils

router = APIRouter(tags=['admin'])

@router.get("/admin/login")
async def admin_login_pg(request: Request):
    return templates.TemplateResponse(
        request,
        "admin/admin_login.html",
    )

@router.get("/admin")
async def admin_pg(request: Request):
    return templates.TemplateResponse(
        request,
        "admin/admin_main.html",
    )