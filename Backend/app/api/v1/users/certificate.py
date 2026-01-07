from sre_parse import CATEGORY_UNI_DIGIT
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Dict, Any
from pydantic import BaseModel
import uuid
from app.schemas.globaltypes import APIResponse
from app.config.database import get_db
from app.controllers.auth.auth_controllers import verify_token_logic
from app.controllers.certificates.certificates_controller import (
    upload_certificate as upload_certificate_controller,
    complete_certificate as complete_certificate_controller
)

router = APIRouter(
    prefix="/users/certificates",
    tags=["User Certificates"]
)

class ParsedData(BaseModel):
        nama_mahasiswa: str = ""
        event_name: str = ""
        rank_raw: str = ""
        level_raw: str = ""
        date_issued: str = ""
        category_raw: str = ""
        domain_raw: str = ""
        confidence: float = 0.0

class SubmitRequest(BaseModel):
    document_id: str
    parsed: ParsedData

class UploadResponse(BaseModel):
    document_id: str = ""
    nama_event: str = ""
    domain: str = ""
    category: str = ""
    rank: str = ""
    level: str = ""
    date: str = ""

@router.post("/upload", response_model=APIResponse)
async def upload_certificate(
    file: UploadFile = File(...),
    user_payload: Dict[str, Any] = Depends(verify_token_logic)
) -> APIResponse:
    try:
        user_id = user_payload.get("sub")
        result = await upload_certificate_controller(file, user_id)
        
        return APIResponse(
            status_code=200,
            message="Certificate uploaded and parsed successfully",
            data=result
        )
        
    except HTTPException as e:
        return APIResponse(
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )
    except Exception as e:
        return APIResponse(
            status_code=500,
            message="Certificate upload failed",
            error=str(e)
        )

@router.post("/submit", response_model=APIResponse)
async def submit_certificate(
    request: SubmitRequest,
    user_payload: Dict[str, Any] = Depends(verify_token_logic)
) -> APIResponse:

    try:
        user_id = user_payload.get("sub")
        # Note: complete_certificate_controller typically might need user_id, 
        # but here it seems to use the request dict. 
        # If the controller relies on implicit user context, it should be passed.
        # However, checking the controller signature previously, it takes request.dict().
        # We just secure the endpoint here.
        processed_data = await complete_certificate_controller(request.dict())
        
        return APIResponse(
            status_code=200,
            message="Certificate submitted successfully",
            data=processed_data
        )
        
    except HTTPException as e:
        return APIResponse(
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )
    except Exception as e:
        return APIResponse(
            status_code=500,
            message="Certificate submission failed",
            error=str(e)
        )