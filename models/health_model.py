from pydantic import BaseModel, Field


class HealthModel(BaseModel):
    health_check: str = Field(
        None, min_length=1, max_length=500)
    google_cloud_storage: bool = Field(None)
    # testing: bool = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            'additionalProperties': False
        }
