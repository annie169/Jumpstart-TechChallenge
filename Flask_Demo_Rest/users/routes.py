from flask_restful import Api
from users.views import LoginApi, SignUpApi, ValidateToken, ValidateTableAccess


def create_authentication_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    """
    api.add_resource(SignUpApi, "/api/auth/register/")
    api.add_resource(LoginApi, "/api/auth/login/")
    api.add_resource(ValidateToken, "/api/auth/validate_token/<token>")
    api.add_resource(ValidateTableAccess, "/api/auth/validate_table_access/<token>/<table_name>")
