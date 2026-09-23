from contextlib import asynccontextmanager
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from Database import database
import utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.InitDatabase()

    yield

    await database.engine.dispose()


app = FastAPI(debug=True, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/presentation_asset", StaticFiles(directory="presentation_asset"), name="/presentation_asset")

templates = Jinja2Templates(directory="templates")
templates_present = Jinja2Templates(directory="templates/presentations")


@app.get("/favicon.ico")
def favic():
    return None


@app.get("/")
def mainpg(request: Request):
    return templates.TemplateResponse(request, "main_page.html")


@app.get("/presentations")
async def prsentationpg(request: Request):
    presentations = utils.get_presentationlist(await database.PresentationDatabase.GetAllPresentations())
    print(presentations)

    return templates.TemplateResponse(
        request,
        "presentation_page.html",
        context={"presentations": presentations},
    )


@app.get("/achievments")
def achievmentspg(request: Request):
    return templates.TemplateResponse(request, "achievments_page.html")


@app.get("/presentation/{present_id}")
async def presentationgt(present_id: int, request: Request):
    present = await database.PresentationDatabase.GetPresentationByID(present_id)
    if present is None:
        return templates.TemplateResponse(request, "main_page.html")
    if os.path.exists(os.path.join("templates/presentations", present.html_file)):
        if "html" in present.html_file.split("."):
            return templates_present.TemplateResponse(request, present.html_file)
        else:
            return FileResponse(
            path=f"presentations/{present.html_file}",
            media_type="application/pdf",
            filename=f"presentation_{id}.pdf"
        )

    else:
        return templates.TemplateResponse(request, "main_page.html")



if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)