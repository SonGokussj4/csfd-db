#!/bin/bash/env python3

from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    print("[ DEBUG ] : Healthcheck called")
    return {"status": "ok"}
