#!/bin/bash/env python3

import sys
from pathlib import Path

from aiofiles import open as aio_open
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

UPLOAD_DIR = Path().cwd() / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="csfd_db/templates")

app = FastAPI(
    # Default TryItOut button enable
    title="Fake CSFD db API",
    description="This is a very simple API for testing purposes",
    version="0.1.0",
    swagger_ui_parameters={
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
        "displayOperationId": True,
    },
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    current_python_version = sys.version
    return {"message": "Hi there, hello", "python_version": current_python_version}


@app.get("/healthcheck")
async def healthcheck():
    print("[ DEBUG ] : Healthcheck called")
    return {"status": "ok"}


@app.get("/uploadfile")
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/uploadfile")
async def handle_file_upload(file_upload: UploadFile):
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_upload.filename

    async with aio_open(save_to, "wb") as f:
        await f.write(data)

    return {"filename": file_upload.filename}
