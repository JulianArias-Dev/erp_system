from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.config import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
   
    # Relación con Product
    product = relationship("Product", back_populates="orders")