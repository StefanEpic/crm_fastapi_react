from fastapi import HTTPException, status

ERROR_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization credentials")
ERROR_404 = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
