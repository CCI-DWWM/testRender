from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import getMsg

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse("index.html")


app.mount("/", StaticFiles(directory="static"), name="static")
