from pydantic import BaseModel, Field
from typing import List, Union
from datetime import datetime

class DecodedToken(BaseModel):
    iss: str
    sub: str
    aud: List[str]
    iat: int
    exp: int
    scope: str
    azp: str

    # Optional method to convert UNIX timestamps to datetime
    def convert_timestamps(self):
        self.iat = datetime.fromtimestamp(self.iat)
        self.exp = datetime.fromtimestamp(self.exp)

class TokenData(BaseModel):
    decoded_token: DecodedToken
    token: str
    
    def __hash__(self):
        # Use hash of token as the hash value
        return hash(self.token)

    def __eq__(self, other):
        # Compare TokenData objects based on token value
        return isinstance(other, TokenData) and self.token == other.token