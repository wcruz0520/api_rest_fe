from sqlalchemy.orm import Session
from .models import Usuario
from .schemas import UsuarioCreate

def get_user_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db: Session, user: UsuarioCreate, password_hash: str):
    db_user = Usuario(
        usuario=user.usuario,
        password_hash=password_hash,
        identificacion=user.identificacion,
        tipo_identificacion=user.tipo_identificacion,
        razon_social=user.razon_social,
        nombre_comercial=user.nombre_comercial,
        correo=user.correo,
        telefono=user.telefono,
        activo=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user