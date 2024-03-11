from modules.data_processing import process_image

from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
import random
from PIL import Image
import datetime
from fastapi.openapi.docs import get_swagger_ui_html
import pandas as pd

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/docs")
def read_docs():
    return get_swagger_ui_html(title='title', openapi_url="/openapi.json")

@app.post("/api")
async def upload(file: UploadFile = File(...)):
    
    contents = await file.read()
    print(type(contents))
    image = Image.open(BytesIO(contents))
    result = {}
    result['is_completed'] = True
    result['numbers'] = process_image(image)
    result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    return result