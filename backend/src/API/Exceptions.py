from fastapi import HTTPException, status


class ServerError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class SQLalchemyError(ServerError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "SQLAlchemy error"
