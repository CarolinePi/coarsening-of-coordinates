from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    full_name = fields.Str(required=True)
    password = fields.Str(required=True)


class LocationSchema(Schema):
    latitude = fields.Decimal(
        required=True, validate=validate.Range(min=-180, max=180)
    )
    longitude = fields.Decimal(
        required=True, validate=validate.Range(min=-90, max=90)
    )


class RegisterRequestSchema(UserSchema):
    location = fields.Nested(LocationSchema, required=True)


class LoginRequestSchema(UserSchema):
    ...


class GetUserResponseSchema(Schema):
    id = fields.Int(required=True)
    full_name = fields.Str(required=True)
    location = fields.Nested(LocationSchema, required=True)
