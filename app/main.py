#!/bin/bash/env python3

import sys

from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    print("[ DEBUG ] : Healthcheck called")
    return {"status": "ok"}


@app.get("/")
def root():
    current_python_version = sys.version
    return {"message": "Hi there, hello", "python_version": current_python_version}
