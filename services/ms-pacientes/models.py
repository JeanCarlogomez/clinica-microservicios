from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cedula = Column(String, unique=True, index=True)
    email = Column(String)
    telefono = Column(String)


class PacienteCreate(BaseModel):
    nombre: str
    cedula: str
    email: str
    telefono: str


class PacienteRead(BaseModel):
    id: int
    nombre: str
    cedula: str
    email: str
    telefono: str

    class Config:
        from_attributes = True
