from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from database_sql import create_db_and_tables, get_db
from models import Usuario, UsuarioCreate, UsuarioRead, LoginRequest, TokenResponse

app = FastAPI(title="Servicio de Autenticacion")
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_temporal")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Servicio de Autenticacion en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/auth/registro", response_model=UsuarioRead)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hash_pw = pwd_context.hash(usuario.password)
    db_usuario = Usuario(email=usuario.email, password_hash=hash_pw, rol=usuario.rol)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.post("/auth/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if not usuario or not pwd_context.verify(datos.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": usuario.email, "rol": usuario.rol, "exp": expiracion},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": token}


app.include_router(router, prefix="/api/v1")
