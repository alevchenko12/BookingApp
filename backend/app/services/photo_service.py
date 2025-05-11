import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_FOLDER = "static/uploads"

def save_image_to_disk(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(file.file.read())

    return filename

def generate_image_url(filename: str) -> str:
    # Fix: Return full absolute URL
    return f"http://10.0.2.2:8000/static/uploads/{filename}"

def delete_image_file(image_url: str):
    filename = image_url.split("/")[-1]
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
