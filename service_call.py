import requests
import json
import logging

from constants import SERVICE_NOW_API_ENDPOINT, SECRET_API_KEY

log = logging.getLogger(__name__)



def get_id_from_api(item):
    try:
        url = f"{SERVICE_NOW_API_ENDPOINT}/create/service_id"
        #validation
        headers = {"Content-Type": "application/json; charset=utf-8",
                   "x-api-key": SECRET_API_KEY
                   }
        # if item is model
        # data = {
        #     "name": item.name,
        #     "description": item.description,
        #     "passion": "coding",
        # }
        response = requests.post(url, headers=headers, json=item)
        # response = requests.post(url, headers=headers, body=json.dumps(item))
        
        log.info("Status Code", response.status_code)
        log.info("JSON Response ", response.json())

        if response.status_code not in [200,201]:
            raise "Get call not sucessful"

        resp = response.json()

        return resp["sys_id"]

    except Exception as e:
        log.error(str(e))
        return "There was an error" + str(e)

def post_files_with_id(sys_id, res):
    try:
        url = f"{SERVICE_NOW_API_ENDPOINT}/upload?service_id={sys_id}"
        headers = {'Content-Type': 'multipart/form-data',"x-api-key": SECRET_API_KEY}

        resp = requests.post(url,headers=headers,data=res)

        if resp.status_code not in  [200,201]:
            #handle failure case
            raise Exception("Post Failed")

        return resp.json()
    except Exception as e:
        log.error(str(e))

