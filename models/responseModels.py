from pydantic import BaseModel, Field
from datetime import date

class UserModel(BaseModel):
    nickname: str
    password: str = Field(exclude=True)
    created_at: date