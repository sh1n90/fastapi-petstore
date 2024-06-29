from typing import List
from pydantic import BaseModel, Field



class Message(BaseModel):
    detail: str = Field(...,
                        min_length=2, max_length=1000)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            'additionalProperties': False
        }



