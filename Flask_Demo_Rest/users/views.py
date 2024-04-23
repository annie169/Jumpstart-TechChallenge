from flask import Response
from flask_restful import Resource
from flask import request, make_response
from users.service import create_user, login_user, validate_token, validate_table_access


class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)


class ValidateToken(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST response method for save new password.

        :return: JSON object
        """
        response, status = validate_token(request, token)
        return make_response(response, status)

class ValidateTableAccess(Resource):
    @staticmethod
    def post(token, table_name) -> Response:
        """
        POST response method for save new password.

        :return: JSON object
        """
        response, status = validate_table_access(request, token, table_name)
        return make_response(response, status)
