from fastapi import HTTPException, status


class KeyNotFoundException(HTTPException):
    def __init__(self, key: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Key {key} not found"
        )