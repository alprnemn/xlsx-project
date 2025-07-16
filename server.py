from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from utils import fetch_data_from_external_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_csv_file(file: UploadFile = File(...)):

    df_client = pd.read_csv(io.BytesIO(await file.read()), sep=";")

    df_external_api = fetch_data_from_external_api()

    print("client data type",type(df_client))
    print("df from client",df_client.iloc[0])
    print("---------")
    print("external source data type",type(df_external_api))
    print("df from external source",df_external_api.iloc[1])

    return {
        "size": "success"
    }
