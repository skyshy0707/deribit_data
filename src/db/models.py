from sqlalchemy import (
    Column, 
    DateTime, 
    Float,
    ForeignKey,
    Integer,
    String
)

from db.engine import Base


class Currency(Base):

    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, unique=True)

class Price(Base):

    __tablename__ = "price"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String, ForeignKey("currency.ticker"), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)