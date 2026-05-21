from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database_sql import create_db_and_tables, get_db
from .models import Historial, HistorialCreate, HistorialRead

app = FastAPI(title="Servicio de Historial")
router = APIRouter()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Servicio de Historial en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/historial/", response_model=list[HistorialRead])
def listar_historial(db: Session = Depends(get_db)):
    return db.query(Historial).all()


@router.get("/historial/{historial_id}", response_model=HistorialRead)
def obtener_historial(historial_id: int, db: Session = Depends(get_db)):
    historial = db.query(Historial).filter(Historial.id == historial_id).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial


@router.get("/historial/paciente/{paciente_id}", response_model=list[HistorialRead])
def historial_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return db.query(Historial).filter(Historial.paciente_id == paciente_id).all()


@router.post("/historial/", response_model=HistorialRead)
def crear_historial(historial: HistorialCreate, db: Session = Depends(get_db)):
    db_historial = Historial(**historial.model_dump())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


app.include_router(router, prefix="/api/v1")
