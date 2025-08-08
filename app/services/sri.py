"""Utilities for generating and validating SRI invoices."""

from pathlib import Path
from xml.etree import ElementTree as ET

from app.schemas.invoice import Factura

BASE_DIR = Path(__file__).resolve().parents[2]
XSD_PATH = BASE_DIR / "docs" / "XML y XSD Factura" / "factura_V2.1.0.xsd"
TEMPLATE_XML_PATH = BASE_DIR / "docs" / "XML y XSD Factura" / "factura_V2.1.0.xml"


class SRIValidationError(Exception):
    """Custom exception for SRI validation errors."""


def generate_invoice_xml(invoice: Factura) -> str:
    """Generate an invoice XML document and validate against the SRI schema.

    Parameters
    ----------
    invoice: Factura
        Invoice data.

    Returns
    -------
    str
        XML string representing the invoice.
    """

    tree = ET.parse(TEMPLATE_XML_PATH)
    root = tree.getroot()

    def _set_simple_fields(element: ET.Element, data: dict) -> None:
        for field, value in data.items():
            if value is None:
                continue
            ET.SubElement(element, field).text = str(value)

    # infoTributaria
    info_trib = root.find("infoTributaria")
    info_trib.clear()
    _set_simple_fields(info_trib, invoice.infoTributaria.model_dump())

    # infoFactura with nested structures
    info_fact = root.find("infoFactura")
    info_fact.clear()
    factura_dump = invoice.infoFactura.model_dump()

    totals = factura_dump.pop("totalConImpuestos", [])
    pagos = factura_dump.pop("pagos", [])
    reembolsos = factura_dump.pop("reembolsos", [])
    _set_simple_fields(info_fact, factura_dump)

    if totals:
        tci_el = ET.SubElement(info_fact, "totalConImpuestos")
        for item in totals:
            ti_el = ET.SubElement(tci_el, "totalImpuesto")
            _set_simple_fields(ti_el, item)

    if pagos:
        pagos_el = ET.SubElement(info_fact, "pagos")
        for pago in pagos:
            pago_el = ET.SubElement(pagos_el, "pago")
            _set_simple_fields(pago_el, pago)

    if reembolsos:
        reemb_el = ET.SubElement(info_fact, "reembolsos")
        for reembolso in reembolsos:
            re_el = ET.SubElement(reemb_el, "reembolso")
            detalles = reembolso.pop("detalleImpuestos", [])
            _set_simple_fields(re_el, reembolso)
            if detalles:
                dets_el = ET.SubElement(re_el, "detalleImpuestos")
                for det in detalles:
                    di_el = ET.SubElement(dets_el, "detalleImpuesto")
                    _set_simple_fields(di_el, det)

    # detalles
    detalles_el = root.find("detalles") or ET.SubElement(root, "detalles")
    detalles_el.clear()
    for det in invoice.detalles:
        det_dict = det.model_dump()
        adicionales = det_dict.pop("detallesAdicionales", [])
        impuestos = det_dict.pop("impuestos", [])
        det_el = ET.SubElement(detalles_el, "detalle")
        _set_simple_fields(det_el, det_dict)

        if adicionales:
            das_el = ET.SubElement(det_el, "detallesAdicionales")
            for ad in adicionales:
                da_el = ET.SubElement(das_el, "detAdicional")
                da_el.set("nombre", ad["nombre"])
                da_el.set("valor", ad["valor"])

        if impuestos:
            imps_el = ET.SubElement(det_el, "impuestos")
            for imp in impuestos:
                imp_el = ET.SubElement(imps_el, "impuesto")
                _set_simple_fields(imp_el, imp)

    # retenciones
    if invoice.retenciones:
        ret_el = root.find("retenciones") or ET.SubElement(root, "retenciones")
        ret_el.clear()
        for ret in invoice.retenciones:
            r_el = ET.SubElement(ret_el, "retencion")
            _set_simple_fields(r_el, ret.model_dump())

    # infoAdicional
    if invoice.infoAdicional:
        ia_el = root.find("infoAdicional") or ET.SubElement(root, "infoAdicional")
        ia_el.clear()
        for campo in invoice.infoAdicional:
            ca_el = ET.SubElement(ia_el, "campoAdicional")
            ca_el.set("nombre", campo.nombre)
            ca_el.text = campo.valor

    xml_string = ET.tostring(root, encoding="unicode")

    try:
        import xmlschema
    except ImportError as exc:  # pragma: no cover - best effort if dependency missing
        raise SRIValidationError("xmlschema library is required") from exc

    schema = xmlschema.XMLSchema(XSD_PATH)
    if not schema.is_valid(xml_string):
        errors = "\n".join(str(e) for e in schema.iter_errors(xml_string))
        raise SRIValidationError(errors)
    return xml_string