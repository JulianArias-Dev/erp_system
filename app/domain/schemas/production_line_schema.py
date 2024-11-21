from pydantic import BaseModel
from typing import List
from .worker_shema import WorkerResponse

class ProductionLineResponse(BaseModel):
    id: int
    liquid_capacity: float
    solid_capacity: float
    production_factor: float
    workers: List[WorkerResponse]

    class Config:
        from_attributes = True
