from contextlib import asynccontextmanager
import os

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from templates_config import templates_present, templates
from Routers import presentations
from Database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.InitDatabase()

    yield

    await database.engine.dispose()


app = FastAPI(debug=True, lifespan=lifespan)

# --------------------- mnt dirs
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/presentation_asset", StaticFiles(directory="presentation_asset"), name="presentation_asset")
# -----------------

# ----------------- Routers
app.include_router(presentations.router)
# -----------------

@app.get("/favicon.ico")
def favic():
    return None


@app.get("/")
def mainpg(request: Request):
    return templates.TemplateResponse(request, "main_page.html")



if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)