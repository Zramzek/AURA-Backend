from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from app.schemas.globaltypes import APIResponse
from app.config.database import get_db
from app.controllers.auth.auth_controllers import verify_token_logic
from app.controllers.staff.certificate_controller import (
    get_certificate_list,
    validate_certificate as validate_certificate_controller,
    certificate_detail
)

router = APIRouter(
    prefix="/staff",
    tags=["Certificate"]
)

class CertificateResponse(BaseModel):
    events: List[Dict[str, Any]]

class ValidationResponse(BaseModel):
    id: str
    status: str
    event_name: str
    nama_mahasiswa: str
    validated_at: str
    validated_by: Dict[str, Any]

class CertificateDetail(BaseModel):
    id: str
    status: str
    event_name: str
    category: str
    tingkat: str
    spu: float
    created_at: str
    user: Dict[str, str]

@router.get("/certificate", response_model=APIResponse[CertificateResponse])
async def get_user_certificate(
    staff_payload: Dict[str, Any] = Depends(verify_token_logic)
) -> APIResponse[CertificateResponse]:
    try:
        # Get user history from controller
        events = await get_certificate_list()
        
        # Prepare response
        certificate_data = {
            "events": events,
        }
        
        return APIResponse[CertificateResponse](
            status_code=200,
            message="Certificate retrieved successfully",
            data=certificate_data
        )
        
    except HTTPException as e:
        return APIResponse[CertificateResponse](
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )
    except Exception as e:
        return APIResponse[CertificateResponse](
            status_code=500,
            message="Failed to retrieve certificate data",
            error=str(e)
        )

@router.put("/validate/{certificate_id}", response_model=APIResponse[ValidationResponse])
async def validate_certificate(
    certificate_id: str,
    staff_payload: Dict[str, Any] = Depends(verify_token_logic)
) -> APIResponse[ValidationResponse]:
    try:
        staff_id = staff_payload.get("sub")
        validated = await validate_certificate_controller(certificate_id, staff_id)

        return APIResponse[ValidationResponse](
            status_code=200,
            message="Certificate validated successfully",
            data=validated
        )
    except HTTPException as e:
        return APIResponse[ValidationResponse](
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )
    except Exception as e:
        return APIResponse[ValidationResponse](
            status_code=500,
            message="Failed to validate certificate",
            error=str(e)
        )


@router.get("/validate/{certificate_id}", response_model=APIResponse[CertificateDetail])
async def get_certificate_detail_endpoint(
    certificate_id: str,
    staff_payload: Dict[str, Any] = Depends(verify_token_logic)
) -> APIResponse[CertificateDetail]:
    try:
        certificate_data = await certificate_detail(certificate_id)

        return APIResponse[CertificateDetail](  
            status_code=200,
            message="Certificate detail retrieved successfully",
            data=certificate_data
        )
    except HTTPException as e:
        return APIResponse[CertificateDetail](
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )
    except Exception as e:
        return APIResponse[CertificateDetail](
            status_code=500,
            message="Failed to retrieve certificate detail",
            error=f"Internal error: {str(e)}"
        )
        