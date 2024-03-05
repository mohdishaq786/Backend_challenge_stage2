from fastapi import APIRouter
from src.apis.v1 import store_api, retrive_api,delete_api

router = APIRouter()

router.include_router(store_api.router_v1)
router.include_router(retrive_api.router_v1)
router.include_router(delete_api.router_v1)
