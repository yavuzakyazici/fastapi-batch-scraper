from datetime import datetime
from pydantic import BaseModel

class RegisterUser(BaseModel):
    is_active: int
    email:str
    password:str

class User(RegisterUser):
    id: int

class Token(BaseModel):
    access_token: str | None
    refresh_token: str | None
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
    scopes: list[str] = []

class Log(BaseModel):
    url: str
    timestamp: str
    status_code: int

class ScrapeRequest(BaseModel):
    url: str

class BatchScrapeRequests(BaseModel):
    requests:list