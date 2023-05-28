from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



@app.get("/hello")
def read_root():
    return {"Hello": "World"}



## Run
# uvicorn hello:app --reload