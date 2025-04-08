from fastapi import HTTPException


class BotException(HTTPException):
    status_code = 500
    detail = "BaseController Error"

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class BotNotFound(BotException):
    detail = "BaseController Not Found"
    status_code = 404

    def __init__(self, filters):
        self.detail += filters
        super(BotException, self).__init__(self.status_code, self.detail)


class BotErrorAdd(BotException):
    detail = "BaseController Error, when want to add"


class BotUpdateError(BotException):
    detail = "BaseController Error, when want to update"
