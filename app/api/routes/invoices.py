from fastapi import APIRouter, HTTPException, Response

from app.schemas.invoice import Factura
from app.services.sri import SRIValidationError, generate_invoice_xml

router = APIRouter()


@router.post("/invoices", response_class=Response)
def create_invoice(invoice: Factura) -> Response:
    """Create an electronic invoice and return its XML representation."""
    try:
        xml_content = generate_invoice_xml(invoice)
    except SRIValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return Response(content=xml_content, media_type="application/xml")