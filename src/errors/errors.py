from flask import Blueprint, request
from werkzeug.exceptions import HTTPException


errors = Blueprint('errors', __name__, template_folder='templates')


class BaseException(HTTPException):
    """
    Базоый класс обработки ошибок
    """
    code = 0
    msg = ''
    error_code = 0


    def get_body(self, environ=None, scope=None):
        """
        Возвращает то что будет видеть пользватель при ошибке
        """
        return (
            "<!doctype html>\n"
            "<html lang=en>\n"
            f"<title>{self.code}</title>\n"
            f"<h1>Exception - {(self.code)}</h1>\n"
            f"{self.description}\n"
        )

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
    

class NotFoundError(BaseException):
    code = 404
    description = f'This Page not Found'

class ServerError(BaseException):
    code = 500
    description = 'Sorry, we make a mistak!('
