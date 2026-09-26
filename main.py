from contextlib import asynccontextmanager
import os
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from templates_config import templates_present, templates
from Routers import presentations
from Database import database
from AdminPanel import bot
import path_config


bot_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    path_config.path_tests()
    
    await database.InitDatabase()
    bot_task = asyncio.create_task(bot.run_bot(), name="telegram_admin")

    yield

    await database.engine.dispose()
    bot_task.cancel("Exit")


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