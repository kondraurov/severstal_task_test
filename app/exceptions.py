from fastapi import HTTPException, status


class RollException(HTTPException):
    status_code = 500
    detail = "Произошла ошибка при обработке рулона."

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class RollIdNotFound(RollException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Рулон с указанным ID не найден."


class RollAddFailed(RollException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось добавить рулон."


class RollDeleteFailed(RollException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось удалить рулон."


class RollUpdateFailed(RollException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось обновить данные рулона."
