from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users, invoices
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Emisión de Documentos Electrónicos",
    description="Esta API permite autenticar usuarios, gestionar usuarios y emitir facturas electrónicas.",
    version="1.0.0",
    contact={
        "name": "2gether-soft",
        "url": "https://www.2gether-soft.com",
        "email": "info@2gether-soft.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["usuarios"])
app.include_router(invoices.router, prefix="/api", tags=["facturas"])