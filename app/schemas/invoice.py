"""Pydantic models for SRI electronic invoices."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class InfoTributaria(BaseModel):
    ambiente: str
    tipoEmision: str
    claveAcceso: str
    razonSocial: str
    nombreComercial: str
    ruc: str
    codDoc: str
    estab: str
    ptoEmi: str
    secuencial: str
    dirMatriz: str
    diaEmission: Optional[str] = None
    mesEmission: Optional[str] = None
    anioEmission: Optional[str] = None


class TotalImpuesto(BaseModel):
    codigo: str
    codigoPorcentaje: str
    baseImponible: str
    valor: str
    tarifa: Optional[str] = None


class Pago(BaseModel):
    formaPago: str
    total: str
    plazo: Optional[str] = None
    unidadTiempo: Optional[str] = None


class ReembolsoDetalleImpuesto(BaseModel):
    codigo: str
    codigoPorcentaje: str
    baseImponibleReembolso: str
    tarifa: str
    impuestoReembolso: str


class Reembolso(BaseModel):
    tipoIdentificacionProveedorReembolso: str
    identificacionProveedorReembolso: str
    codPaisPagoProveedorReembolso: str
    tipoProveedorReembolso: str
    codDocReembolso: str
    estabDocReembolso: str
    ptoEmiDocReembolso: str
    secuencialDocReembolso: str
    fechaEmisionDocReembolso: str
    numeroautorizacionDocReemb: str
    detalleImpuestos: List[ReembolsoDetalleImpuesto]


class InfoFactura(BaseModel):
    fechaEmision: str
    dirEstablecimiento: str
    contribuyenteEspecial: Optional[str] = None
    obligadoContabilidad: Optional[str] = None
    tipoIdentificacionComprador: str
    guiaRemision: Optional[str] = None
    razonSocialComprador: str
    identificacionComprador: str
    direccionComprador: str
    totalSinImpuestos: str
    totalDescuento: str
    totalConImpuestos: List[TotalImpuesto]
    propina: Optional[str] = None
    importeTotal: str
    moneda: Optional[str] = None
    pagos: Optional[List[Pago]] = None
    valorRetIva: Optional[str] = None
    valorRetRenta: Optional[str] = None
    comercioExterior: Optional[str] = None
    IncoTermFactura: Optional[str] = None
    lugarIncoTerm: Optional[str] = None
    paisOrigen: Optional[str] = None
    puertoEmbarque: Optional[str] = None
    paisDestino: Optional[str] = None
    paisAdquisicion: Optional[str] = None
    incoTermTotalSinImpuestos: Optional[str] = None
    fleteInternacional: Optional[str] = None
    seguroInternacional: Optional[str] = None
    gastosAduaneros: Optional[str] = None
    gastosTransporteOtros: Optional[str] = None
    codDocReembolso: Optional[str] = None
    totalComprobantesReembolso: Optional[str] = None
    totalBaseImponibleReembolso: Optional[str] = None
    totalImpuestoReembolso: Optional[str] = None
    reembolsos: Optional[List[Reembolso]] = None


class DetalleAdicional(BaseModel):
    nombre: str
    valor: str


class DetalleImpuesto(BaseModel):
    codigo: str
    codigoPorcentaje: str
    baseImponible: str
    valor: str
    tarifa: Optional[str] = None


class Detalle(BaseModel):
    codigoPrincipal: str
    codigoAuxiliar: Optional[str] = None
    descripcion: str
    cantidad: float
    precioUnitario: str
    descuento: str
    precioTotalSinImpuesto: str
    detallesAdicionales: Optional[List[DetalleAdicional]] = None
    impuestos: List[DetalleImpuesto]


class Retencion(BaseModel):
    codigo: str
    codigoPorcentaje: str
    tarifa: str
    valor: str


class CampoAdicional(BaseModel):
    nombre: str
    valor: str


class Factura(BaseModel):
    infoTributaria: InfoTributaria
    infoFactura: InfoFactura
    detalles: List[Detalle]
    retenciones: Optional[List[Retencion]] = None
    infoAdicional: Optional[List[CampoAdicional]] = None