from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
import json
import uvicorn
import logging
from typing import List
from constants import service_now_constant_1, service_now_constant_2, \
    service_now_constant_3, service_now_constant_4, service_now_constant_5



#to read env variable
import os
username = os.getenv("user_key")

from service_call import get_id_from_api, post_files_with_id
from util import validate_file_size

class Item(BaseModel):
    name: str
    description: str | None = None
    application: str

class ServiceNowRequest:
    # normal python class to intilize the item to service_now request
    def __init__(self, item:Item):
        self.name = item.name
        self.description = item.description
        self.application = item.application
        self.const_value_1: str = service_now_constant_1
        self.const_value_2: str = service_now_constant_2
        self.const_value_3: str = service_now_constant_3
        self.const_value_4: str = service_now_constant_4
        self.const_value_5: str = service_now_constant_5


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

@app.post("/insert/")
async def insert_file(item: Item):
    try:
        #just the object alone
        sys_id = get_id_from_api(item)
        sys_id = "sys_id_122323"

        res =  {"item":json.dumps(item)}
        val = post_files_with_id(sys_id, res)
        
        return val
    except Exception as e:
        return HTTPException(400, str(e),{})


class FileInput(BaseModel):
    files: List[UploadFile]

@app.post("/items/")
async def create_item(item: Item, file_input: FileInput):
    files_list = []
    for file in file_input.files:
        contents = await file.read()
        file_dict = {"filename": file.filename, "contents": contents}
        files_list.append(file_dict)
    return {"item": item, "files": files_list}

@app.post("/populate")
# adding a item class to servicenow class
async def populate(item: Item):
    try:

       sreq= ServiceNowRequest(item)
       sreq_dict = vars(sreq)
       id = get_id_from_api(sreq_dict)
       return sreq_dict
    except Exception as e:
        return HTTPException(400, str(e),{})
    
if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, reload=True)