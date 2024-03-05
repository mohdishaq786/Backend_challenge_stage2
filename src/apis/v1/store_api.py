from tasks import store_key_value_to_redis, delete_key_from_redis, huey
from pydantic import BaseModel
from typing import Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tasks import red as redis_client
import logging

logger = logging.getLogger("uvicorn")

router_v1 = APIRouter(prefix="/apis/v1", tags=["v1"], responses={404: {"description": "Not found"}})

class Input(BaseModel):
    key:Any
    value:Any

@router_v1.post("/store")
async def store_key_value_endpoint(input: Input):
    try:
        key = input.key
        value = input.value
        if key == None or value == None:
            out = 'Bad request'
            logger.info("Bad request")
            return JSONResponse(status_code=400, content=jsonable_encoder(out))
        # Properly dispatch the task to Huey
        logger.info("Before store_key_value_to_redis" )
        store_key_value_to_redis(key, value)  # Notice the .delay() here
        out = {key : value}
        logger.info("After store_key_value_to_redis" )

        return JSONResponse(status_code=201, content=jsonable_encoder(out))
    except:
        out = 'Internal Server Error'
        return JSONResponse(status_code=500, content=jsonable_encoder(out)) 
    
