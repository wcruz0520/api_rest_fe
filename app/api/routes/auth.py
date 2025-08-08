from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import create_access_token, verify_password
from app.crud.user import get_user_by_username
from app.schemas.user import UsuarioLogin

router = APIRouter()


@router.post("/login")
def login(data: UsuarioLogin, db: Session = Depends(deps.get_db)):
    user = get_user_by_username(db, data.usuario)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}