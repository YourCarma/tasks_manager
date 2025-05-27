# pylint: disable=E1136
from datetime import datetime

from sqlalchemy.orm import (
    mapped_column, relationship, Mapped
)
from sqlalchemy import String, ForeignKey, Integer, DateTime
from database.base import Base

# Base tables
class Table(Base):
    __tablename__ = "table"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    name = mapped_column(String(30), nullable=False)
    seats = mapped_column(Integer, nullable=False)
    location = mapped_column(String(128), nullable=False)
    
    reservations: Mapped[list["Reservation"]] = relationship("Reservation", back_populates="table", cascade='save-update, merge, delete')
    
    
class Reservation(Base):
    __tablename__ = "reservation"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    customer_name = mapped_column(String(20), nullable=False)
    reservation_time = mapped_column(DateTime, nullable=False, default=datetime.now())
    duration_minutes = mapped_column(Integer, nullable=False)
    table_id = mapped_column(Integer, ForeignKey("table.id"))
    
    table: Mapped[Table] = relationship(
        "Table",
        back_populates="reservations"
    )
    


    
    
    



    
    
    
    
    
    