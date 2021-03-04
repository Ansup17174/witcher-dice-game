from fastapi import HTTPException
import sqlalchemy.exc
import sqlite3
from psycopg2.errors import UniqueViolation
from . import config
import re


auth_exception = HTTPException(detail="Unable to authenticate user", status_code=401)
not_found = HTTPException(detail="Not found", status_code=404)


def get_unique_violation_exception(exc: sqlalchemy.exc.IntegrityError):
    if config.DATABASE_URL == config.DEFAULT_DATABASE_URL:  # sqlite3
        try:
            raise exc.orig
        except sqlite3.IntegrityError as exception:
            message = exception.args[0]
            found = re.search(r".*?\.(\w+)", message)
            column_name = found.group(1)
            return HTTPException(
                detail=f"This {column_name} is already occupied",
                status_code=400
            )
    else:
        try:
            raise exc.orig
        except UniqueViolation as exception:
            found = re.search(r"\((\w+)\)=\((.+)\)", exception.pgerror)
            column_name = found.group(1)
            return HTTPException(
                detail=f"This {column_name} is already occupied",
                status_code=400
            )
