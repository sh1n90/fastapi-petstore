import logging
import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings



log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    
    environment:str
    auth0_client_id:str
    auth0_client_secret:str
    auth0_domain:str
    auth0_audience:str
    auth0_algorithm:str
    auth0_client_id_machine:str
    auth0_client_secret_machine:str
    
    class Config:
        env_file = ".env"



@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
