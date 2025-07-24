from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from utils import (fetch_df_from_external_api,
                   concat_and_filter_dataframes,
                    get_labelids_from_df
                    )


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

    # Convert csv file f rom client to data frame
    df_client = pd.read_csv(io.BytesIO(await file.read()), sep=";")

    # Fetch external data and convert to dataframe
    df_external_api = fetch_df_from_external_api()

    # Concatenate dataframes and filter which does not contain ['hu'] values and duplicated values based on kurzname
    df_result = concat_and_filter_dataframes(df_external_api, df_client)

    # get label ids from label ids column using dataframe before make request for each label ids to get color codes
    label_ids = get_labelids_from_df(df_result)






    return {"message: " : "sv is running.."}
