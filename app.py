from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import json
import uvicorn
import logging
from typing import List


#to read env variable
import os
username = os.getenv("user_key")

from service_call import get_id_from_api, post_files_with_id
from util import validate_file_size

class Item(BaseModel):
    name: str
    description: str | None = None
    application: str

app = FastAPI()
log = logging.getLogger(__name__)

@app.get("/")
async def hello():
    return "hello"


@app.post("/uploadfiles/")
async def create_upload_files(item: Item = Depends(),files: List[UploadFile] = File(...)):
    try:
        #get sys_id
        sys_id = get_id_from_api(item)
        sys_id = "sys_id_122323"

        file_list = []
        for file in files:
            contents = await file.read()
            validate_file_size(contents)
            file_dict = {"filename": file.filename, "contents": contents}
            file_list.append(file_dict)
        res =  {"item":json.dumps(item),"files": file_list}
        val = post_files_with_id(sys_id, res)
        
        return val
    except Exception as e:
        return HTTPException(400, str(e),{})

if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, reload=True)