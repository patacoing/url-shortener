from fastapi import FastAPI
import uvicorn

from app.settings import settings
from app.controller.main_controller import router as main_router

app = FastAPI()

app.include_router(main_router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)