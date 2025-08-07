from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .database import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    identificacion = Column(String(20), nullable=False)
    tipo_identificacion = Column(String(2), nullable=False)
    razon_social = Column(String(120), nullable=False)
    nombre_comercial = Column(String(120))
    correo = Column(String(120), nullable=False)
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())