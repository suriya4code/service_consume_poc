from starlette_validation_uploadfile import ValidateUploadFileMiddleware

from fastapi import (
      FastAPI, 
      Path, 
      File, 
      UploadFile, 
 ) 


app = FastAPI()

#add this after FastAPI app is declared 
app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/",
        max_size=1048576, #1Mbyte
        file_type=["text/plain"]
)


@app.post("/")
async def root(file: UploadFile  = File(...)):
    #...do something with the file
    return {"status: upload successful"}