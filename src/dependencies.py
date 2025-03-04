from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "1234"
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


__all__ = ["verify_api_key"]
