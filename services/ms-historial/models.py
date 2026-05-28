from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, index=True)
    diagnostico = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)
    notas = Column(String)


class HistorialCreate(BaseModel):
    paciente_id: int
    diagnostico: str
    fecha: Optional[datetime] = None
    notas: Optional[str] = None


class HistorialRead(BaseModel):
    id: int
    paciente_id: int
    diagnostico: str
    fecha: datetime
    notas: Optional[str] = None

    class Config:
        from_attributes = True
