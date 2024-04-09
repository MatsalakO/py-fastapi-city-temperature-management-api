from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from temperature.models import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    additional_info = Column(String(255))
    temperatures = relationship("DBTemperature", back_populates="city")