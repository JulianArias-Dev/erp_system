from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    uid = Column(String(100), unique=True, nullable=False)
    fk_production_line = Column(Integer, ForeignKey("production_lines.id", ondelete="SET NULL"))

    # Relación con ProductionLine
    production_line = relationship("ProductionLine", back_populates="workers")
