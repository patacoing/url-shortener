from fastapi import HTTPException, status

class CallCountExceededException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached too many calls"
        )
