from marshmallow import Schema, fields, validate

class TalkValidationSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=100))