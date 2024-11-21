from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from app.config import Base

class ProductionLine(Base):
    __tablename__ = "production_lines"

    id = Column(Integer, primary_key=True, index=True)
    liquid_capacity = Column(Float, nullable=False)
    solid_capacity = Column(Float, nullable=False)
    production_factor = Column(Float, nullable=False)

    # Relación con Workers
    workers = relationship("Worker", back_populates="production_line")
