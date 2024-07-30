from typing import Union
from fastapi import FastAPI

from app.settings import settings
from app.database.redis import redis

app = FastAPI()

@app.get("/")
def read_redis():
    redis.set("key", "value")
    return redis.get("key")