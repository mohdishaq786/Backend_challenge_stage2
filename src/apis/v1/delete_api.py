
from tasks import  delete_key_from_redis, huey
from pydantic import BaseModel
from typing import Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tasks import red as redis_client

router_v1 = APIRouter(prefix="/apis/v1", tags=["v1"], responses={404: {"description": "Not found"}})


class KeyInput(BaseModel):
    key: Any

@router_v1.delete("/delete")
async def delete_key_endpoint(input: KeyInput):
    try:
        key = input.key
        
        if not redis_client.exists(key):
            return JSONResponse(status_code=404, content=jsonable_encoder("Key not found"))

        if key is None:
            return JSONResponse(status_code=400, content=jsonable_encoder('Bad request'))
        # Dispatch the delete task to Huey
        delete_key_from_redis(key)
        return JSONResponse(status_code=200, content=jsonable_encoder(f'Key {key} scheduled for deletion'))
    except Exception as e:
        return JSONResponse(status_code=500, content=jsonable_encoder('Internal Server Error'))