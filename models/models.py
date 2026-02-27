from pydantic import BaseModel, Field
from datetime import date

class InheritanceModel(BaseModel):
    is_published: bool = Field(default=True)

    created_at: date = Field(default_factory=lambda: date.today())