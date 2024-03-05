import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.routes.v1_router import router as router_v1
import redis
import logging

logger = logging.getLogger("uvicorn")
app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your application's router
app.include_router(router_v1)

# Initialize Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.on_event("startup")
async def startup_event():
    try:
        # Attempt to ping Redis
        response = redis_client.ping()
        print(f"Redis connection test: {response}")
    except Exception as e:
        print(f"Redis connection error: {e}")
        raise HTTPException(status_code=500, detail="Unable to connect to Redis.")


if __name__ == "__main__":
    print("Starting application...")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, workers=1, reload=False)


