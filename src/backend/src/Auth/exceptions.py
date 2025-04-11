from fastapi import HTTPException
from fastapi import status


class AuthError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ""

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class UserNotFound(AuthError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found: "

    def __init__(self, filters: dict):
        self.detail += str(filters)
        super(AuthError, self).__init__(self.status_code, self.detail)


class UserAlreadyExists(AuthError):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class JWTExpired(AuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT Expired"


class JWTNotFound(AuthError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "JWT Not Found"


class JWTError(AuthError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "JWT Error"


class ReLogin(AuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Re-login required"


class PasswordInvalid(AuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Password must be at least 8 characters long, and contain only Upper/Lower letters, numbers"


class PasswordNotMatch(AuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Password not match"
