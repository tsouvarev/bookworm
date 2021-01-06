from marshmallow import Schema, fields


class BookSchema(Schema):
    id = fields.String()
    author = fields.String()
    title = fields.String()
    pages_number = fields.Integer()
    date_start = fields.Date()
    date_end = fields.Date()
    comment = fields.String()


class AddBoookSchema(Schema):
    author = fields.String(required=True)
    title = fields.String(required=True)
    pages_number = fields.Integer(required=True)
    date_start = fields.Date()
    date_end = fields.Date()
    comment = fields.String()
