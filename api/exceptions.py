from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import re


auth_exception = HTTPException(detail="Unable to authenticate user", status_code=401)
not_found = HTTPException(detail="Not found", status_code=404)


def get_unique_violation_exception(exc: IntegrityError):
    try:
        raise exc.orig
    except UniqueViolation as exception:
        found = re.search(r"\((\w+)\)=\((.+)\)", exception.pgerror)
        column_name = found.group(1)
        return HTTPException(
            detail=f"This {column_name} is already occupied",
            status_code=400
        )
