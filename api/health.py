from functools import lru_cache
from fastapi import APIRouter, Depends, Security
from fastapi import status
from config import Settings,get_settings
from models.health_model import HealthModel
from models.message_model import Message
from utils.oauth import get_current_user,get_current_user_info

router = APIRouter()
settings: Settings = get_settings()






@router.get("/health", status_code=status.HTTP_200_OK,
            response_model=HealthModel, responses={
                403: {"model": Message},
                404: {"model": Message},
                406: {"model": Message}
            },
            openapi_extra={"x-42c-no-authentication": True},

            )
def get_secure(user = Depends(get_current_user_info)):
    print( {"message": f"{user}"})

    health_check = "OK!"
    google_cloud_storage = True
    try:
        print("health_check_ok")
    except Exception as e:
        health_check = "KO - GCS access denied : " + str(e)
        

    response = {
        "health_check": health_check,
        "google_cloud_storage": google_cloud_storage,

    }
    return HealthModel(**response)