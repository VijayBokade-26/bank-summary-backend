from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.setu_service import setu_login

router = APIRouter()


class LoginRequest(BaseModel):
    """Dynamic login request - client provides all data."""
    clientID: str
    grant_type: str
    secret: str
    # Allow extra fields
    model_config = {"extra": "allow"}


def validate_and_extract_headers(request: Request, payload: Dict) -> Dict:
    extracted_headers = {}
    
    # Extract headers from HTTP request headers
    if request:
        # Extract headers that client provided
        headers_to_include = ["content-type", "client"]
        for key, value in request.headers.items():
            key_lower = key.lower()
            if any(key_lower.startswith(h) for h in headers_to_include):
                # Validate header value is not empty
                if not value or not str(value).strip():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Header '{key}' cannot be empty"
                    )
                extracted_headers[key] = value
    
    # If no client header provided in request, check in payload
    if "client" not in extracted_headers and "client" in payload:
        client_value = payload.get("client")
        if not client_value or not str(client_value).strip():
            raise HTTPException(
                status_code=400,
                detail="Header 'client' cannot be empty"
            )
        extracted_headers["client"] = client_value
        payload.pop("client")
    
    # Validate client header exists
    if "client" not in extracted_headers:
        raise HTTPException(
            status_code=400,
            detail="Missing required header: 'client'"
        )
    
    # Ensure Content-Type is always application/json
    if "content-type" not in extracted_headers and "Content-Type" not in extracted_headers:
        extracted_headers["Content-Type"] = "application/json"
    else:
        # Validate if content-type was provided
        provided_content_type = extracted_headers.get("content-type") or extracted_headers.get("Content-Type")
        if "json" not in provided_content_type.lower():
            raise HTTPException(
                status_code=400,
                detail="Content-Type must be 'application/json'"
            )
    
    return extracted_headers

def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": False,
            "status_code": status_code,
            "error": message
        }
    )

@router.post("/setu/login", status_code=201)
async def login(request_body: LoginRequest, request: Request):
    payload = request_body.model_dump()
    extracted_headers = validate_and_extract_headers(request, payload)
    data = setu_login(payload, extracted_headers)
    return {
        "status": True,
        "status_code": 201,
        "data": data,
        "msg": "Token generated Successfully!!"
    }


# @router.post("/setu/login")
# async def login(
#     request_body: LoginRequest,
#     request: Request
# ):
#     # Convert request body to dict
#     payload = request_body.model_dump(exclude_none=False)
#     try:
#         extracted_headers = validate_and_extract_headers(request, payload)
#     except HTTPException as e:
#         return error_response(
#             e.status_code,
#             e.detail
#         )
#     except Exception as e:
#         return error_response(
#             400,
#             f"Header validation error: {str(e)}"
#         )

#     # Validate required payload fields
#     if not payload.get("clientID") or not str(payload.get("clientID")).strip():
#         return error_response(
#             400,
#             "Missing or empty required field: clientID"
#         )

#     if not payload.get("grant_type") or not str(payload.get("grant_type")).strip():
#         return error_response(
#             400,
#             "Missing or empty required field: grant_type"
#         )

#     if not payload.get("secret") or not str(payload.get("secret")).strip():
#         return error_response(
#             400,
#             "Missing or empty required field: secret"
#         )

#     # Call Setu login service
#     try:
#         result = setu_login(payload, extracted_headers)

#         # If service layer returns error
#         if isinstance(result, dict) and "error" in result:
#             return error_response(
#                 result.get("status_code", 500),
#                 result.get("error")
#             )

#         return result

#     except Exception as e:
#         return error_response(
#             500,
#             f"Login failed: {str(e)}"
#         )




