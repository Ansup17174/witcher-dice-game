from fastapi import HTTPException


auth_exception = HTTPException(detail="Unable to authenticate user", status_code=401)
