import os

from fastapi.requests import Request
from aiogram import html
import bcrypt

from Database import models

get_filetype = lambda file_name: file_name.rsplit(".", 1)[-1].lower() if "." in file_name else None

def get_presentationlist(presentations: list[models.Presentation], request: Request):
    presentationks = []

    for present in presentations:
        presentationks.append({
            "id": present.id,
            "title": present.name,
            "authors": present.author,
            "description": present.description,
            "cover": request.url_for("presentation_asset", path=os.path.join("preview_img/", present.preview_image))._url if present.preview_image else None,
            "file_type": get_filetype(present.file)
        })

    return presentationks

def get_localpresentations_msg(first_name: str, presentations: list[models.Presentation]) -> str:
    presentations_msg = f"{html.bold(first_name)}, Все презентации\n"

    for present in presentations:
        msg = f"""[#] ID: {html.bold(present.id)}
[#] Название: {present.name}
[#] Авторы: {present.author}
[#] Изображение: {present.preview_image}
[#] Фаил: {present.file}
----"""
        presentations_msg += msg + "\n"

    return presentations_msg

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashpwd = bcrypt.hashpw(password_bytes, salt)
    return hashpwd.decode('utf-8')

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))    
