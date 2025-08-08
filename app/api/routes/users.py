from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import get_password_hash
from app.crud.user import create_user, get_user_by_username
from app.models.user import Usuario
from app.schemas.user import UsuarioCreate, UsuarioOut

router = APIRouter()


@router.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(
    usuario: UsuarioCreate, db: Session = Depends(deps.get_db)
):
    db_user = get_user_by_username(db, usuario.usuario)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    password_hash = get_password_hash(usuario.password)
    return create_user(db, usuario, password_hash)


@router.get("/usuarios/me", response_model=UsuarioOut)
def get_me(user: Usuario = Depends(deps.get_current_user)):
    return user