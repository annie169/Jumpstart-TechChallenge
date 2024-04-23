import json
import jwt
import datetime
from server import db
from os import environ
from users.models import User
from flask_bcrypt import generate_password_hash
from utils.common import generate_response, TokenGenerator
from users.validation import (
    CreateLoginInputSchema,
    CreateSignupInputSchema,
)


def create_user(request, input_data):
    """
    It creates a new user

    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.query.filter_by(
        username=input_data.get("username")
    ).first()
    check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
    if check_username_exist:
        return generate_response(
            message="Username already exist", status=400
        )
    elif check_email_exist:
        return generate_response(
            message="Email  already taken", status=400
        )

    new_user = User(**input_data)  # Create an instance of the User class
    new_user.hash_password()
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Comment
    del input_data["password"]
    return generate_response(
        data=input_data, message="User Created", status=201
    )


def login_user(request, input_data):
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response

    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A dictionary with the keys: data, message, status
    """
    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    get_user = User.query.filter_by(email=input_data.get("email")).first()
    if get_user is None:
        return generate_response(message="User not found", status=400)
    if get_user.check_password(input_data.get("password")):
        token = jwt.encode(
            {
                "id": get_user.id,
                "email": get_user.email,
                "username": get_user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            environ.get("SECRET_KEY"),
        )
        input_data["token"] = token
        return generate_response(
            data=input_data, message="User login successfully", status=201
        )
    else:
        return generate_response(
            message="Password is wrong", status=400
        )


def validate_token(request, token):
    if not token:
        return generate_response(
            message="Token is required!",
            status=400,
        )
    token_status = TokenGenerator.check_token(token)
    if token_status:
        token = TokenGenerator.decode_token(token)
        user = User.query.filter_by(id=token.get('id')).first()
        if user is None:
            return generate_response(
                message="No record found with this email. please signup first.",
                status=400,
            )
        user = User.query.filter_by(id=token['id']).first()
        if user:
            return generate_response(
                message="Token validated", status=200
            )
    else:
        return generate_response(
            message="Failed to validate token",
            status=400,
        )

def validate_table_access(request, token, table_name):
    if not token:
        return generate_response(
            message="Token is required!",
            status=400,
        )

    token_status = TokenGenerator.check_token(token)

    if token_status:
        decoded_token = TokenGenerator.decode_token(token)
        user_id = decoded_token.get('id')

        if not user_id:
            return generate_response(
                message="Invalid token format. Please log in again.",
                status=400,
            )

        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return generate_response(
                message="No user found with this ID. Please sign up first.",
                status=400,
            )

        access = set(user.access_map.split(','))

        if table_name in access:
            return generate_response(
                message="You have access to " + table_name,
                status=200,
            )
        else:
            return generate_response(
                message="No access to " + table_name + "table",
                status=403,
            )
    else:
        return generate_response(
            message="Failed to validate token",
            status=400,
        )