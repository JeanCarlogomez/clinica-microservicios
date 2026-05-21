from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, index=True)
    fecha = Column(DateTime)
    medico = Column(String)
    estado = Column(String, default="programada")


class CitaCreate(BaseModel):
    paciente_id: int
    fecha: datetime
    medico: str
    estado: Optional[str] = "programada"


class CitaRead(BaseModel):
    id: int
    paciente_id: int
    fecha: datetime
    medico: str
    estado: str

    class Config:
        from_attributes = True
