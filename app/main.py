from fastapi import FastAPI, Depends, HTTPException, status
from app import models, schemas, crud, auth, dependencies
from app.database import engine, Base
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringe para producción si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/usuarios", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, usuario.usuario)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    password_hash = auth.get_password_hash(usuario.password)
    return crud.create_user(db, usuario, password_hash)

@app.post("/api/auth/login")
def login(data: schemas.UsuarioLogin, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user_by_username(db, data.usuario)
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = auth.create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/usuarios/me", response_model=schemas.UsuarioOut)
def get_me(user: models.Usuario = Depends(dependencies.get_current_user)):
    return user