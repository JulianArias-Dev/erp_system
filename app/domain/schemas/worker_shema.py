from pydantic import BaseModel, Field
from typing import Optional

class WorkerCreate(BaseModel):
    name: str = Field(..., max_length=255)
    uid: str = Field(..., max_length=100)
    fk_production_line: Optional[int]

class WorkerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    uid: Optional[str] = Field(None, max_length=100)
    fk_production_line: Optional[int]

class WorkerResponse(BaseModel):
    id: int
    name: str
    uid: str
    fk_production_line: Optional[int]

    class Config:
        from_attributes = True
