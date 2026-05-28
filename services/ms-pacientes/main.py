from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database_sql import create_db_and_tables, get_db
from models import Paciente, PacienteCreate, PacienteRead

app = FastAPI(title="Servicio de Pacientes")
router = APIRouter()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Servicio de Pacientes en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/pacientes/", response_model=list[PacienteRead])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()


@router.get("/pacientes/{paciente_id}", response_model=PacienteRead)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@router.post("/pacientes/", response_model=PacienteRead)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente


@router.delete("/pacientes/{paciente_id}")
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente eliminado"}


app.include_router(router, prefix="/api/v1")
