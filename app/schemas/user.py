from typing import Optional

from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    usuario: str
    password: str
    identificacion: str
    tipo_identificacion: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    correo: EmailStr
    telefono: Optional[str] = None

class UsuarioLogin(BaseModel):
    usuario: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    usuario: str
    identificacion: str
    tipo_identificacion: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    correo: EmailStr
    telefono: Optional[str] = None
    activo: bool

    class Config:
        orm_mode = True