from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tasks import retrieve_value_from_redis, huey  # Assuming these are defined properly
from typing import Any
from pydantic import BaseModel
import traceback
from tasks import red as redis_client

router_v1 = APIRouter(prefix="/apis/v1", tags=["v1"], responses={404: {"description": "Not found"}})

class Input(BaseModel):
    key: Any

@router_v1.get("/retrieve")
async def retrieve_value_endpoint(input: Input):
    try:
        key = input.key
        if key is None:
            out = 'Bad request'
            return JSONResponse(status_code=400, content=jsonable_encoder(out))
        value = retrieve_value_from_redis(key)
        # Set a timeout for the blocking call

        if not redis_client.exists(key):
            return JSONResponse(status_code=404, content=jsonable_encoder("Key not found"))

        value = value.get(blocking=True, timeout=5)  # Timeout after 5 seconds
        
        out = {"key": key, "value": value}
        return JSONResponse(status_code=200, content=jsonable_encoder(out))
    except:
        out = traceback.format_exc()
        return JSONResponse(status_code=500, content=jsonable_encoder(out))
