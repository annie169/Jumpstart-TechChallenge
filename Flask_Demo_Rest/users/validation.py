from marshmallow import Schema, fields, validate


class CreateSignupInputSchema(Schema):
    # the 'required' argument ensures the field exists
    username = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    type = fields.Str(required=True)
    access_map = fields.Str(required=True)



class CreateLoginInputSchema(Schema):
    # the 'required' argument ensures the field exists
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
