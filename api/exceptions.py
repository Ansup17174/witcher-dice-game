from fastapi import HTTPException


auth_exception = HTTPException(detail="Unable to authenticate user", status_code=401)
not_found = HTTPException(detail="Not found", status_code=404)
