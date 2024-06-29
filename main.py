
import logging

from typing import List
from fastapi import BackgroundTasks, FastAPI, Request, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.background import BackgroundTask
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api import health
from config import Settings, get_settings

settings: Settings = get_settings()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
logger.info("GoldenData backend has been started")


def create_application() -> FastAPI:
    
    swagger_ui_init_oauth={
            "clientId": settings.auth0_client_id,
            "clientSecret": settings.auth0_client_secret,
            "audience": settings.auth0_audience,
            "grant_type": "client_credentials"
        }

    app = FastAPI(
        swagger_ui_init_oauth=swagger_ui_init_oauth,
    )
    app.include_router(health.router)


    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_application()


@app.on_event("startup")
async def get_gcp_sa():
    print()
