from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from schemas.globaltypes import APIResponse
from fastapi.responses import JSONResponse

from controllers.auth.auth_controllers import login_user, verify_token_logic, refresh_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=APIResponse)
async def login(request: LoginRequest):
    try:
        result = await login_user(request.username, request.password)

        return APIResponse(
            status_code=200,
            message="Login successful",
            data=result
        )

    except HTTPException as e:
        return APIResponse(
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )

@router.post("/logout", response_model=APIResponse)
async def logout(user: Dict[str, Any] = Depends(verify_token_logic)):
    return APIResponse(
        status_code=200,
        message="Logout successful",
        data=None
    )

@router.post("/refresh", response_model=APIResponse)
async def refresh_token(request: RefreshRequest):
    try:
        result = await refresh_access_token(request.refresh_token)
        return APIResponse(
            status_code=200,
            message="Token refreshed successfully",
            data=result
        )
    except HTTPException as e:
        return APIResponse(
            status_code=e.status_code,
            message=e.detail,
            error=str(e.detail)
        )


@router.get("/verify", response_model=APIResponse)
async def verify_token(user: Dict[str, Any] = Depends(verify_token_logic)):
    return APIResponse(
        status_code=200,
        message="Token is valid",
        data={
            "user_id": user.get("sub"),
            "email": user.get("email"),
            "role": user.get("role")
        }
    )

@router.get("/me", response_model=APIResponse)
async def get_my_profile(user: Dict[str, Any] = Depends(verify_token_logic)):
    return APIResponse(
        status_code=200,
        message="Profile retrieved successfully",
        data={
            "user": user
        }
    )