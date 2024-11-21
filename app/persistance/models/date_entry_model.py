from sqlalchemy import Column, String, DateTime
from app.config import Base

class DateEntry(Base):
    __tablename__ = "dates"

    name = Column(String(50), primary_key=True)
    date = Column(DateTime, nullable=False)
