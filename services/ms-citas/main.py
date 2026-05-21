from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database_sql import create_db_and_tables, get_db
from .models import Cita, CitaCreate, CitaRead

app = FastAPI(title="Servicio de Citas")
router = APIRouter()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Servicio de Citas en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/citas/", response_model=list[CitaRead])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()


@router.get("/citas/{cita_id}", response_model=CitaRead)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


@router.post("/citas/", response_model=CitaRead)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    db_cita = Cita(**cita.model_dump())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita


@router.delete("/citas/{cita_id}")
def cancelar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"message": "Cita cancelada"}


app.include_router(router, prefix="/api/v1")
