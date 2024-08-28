#!/bin/bash/env python3

import sys
from pathlib import Path

from aiofiles import open as aio_open
from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from csfd_db import auth, models, schemas
from csfd_db.db import engine
from csfd_db.routes import router

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

models.Base.metadata.create_all(bind=engine)
app.include_router(router)


@app.get("/", dependencies=[Depends(auth.get_current_user)], include_in_schema=False)
async def root():
    current_python_version = sys.version
    return {"message": "Hi there, hello", "python_version": current_python_version}


@app.get("/healthcheck")
async def healthcheck():
    print("[ DEBUG ] : Healthcheck called")
    return {"status": "ok"}


@app.get("/auth-check/")
async def auth_check(current_user: schemas.UserInDB = Depends(auth.get_current_user)):
    return current_user


@app.get("/uploadfile", dependencies=[Depends(auth.get_current_user)])
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/uploadfile", dependencies=[Depends(auth.get_current_user)])
async def handle_file_upload(file_upload: UploadFile):
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_upload.filename

    async with aio_open(save_to, "wb") as f:
        await f.write(data)

    return {"filename": file_upload.filename}
