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


class EditBoookSchema(Schema):
    author = fields.String(allow_none=True)
    title = fields.String(allow_none=True)
    pages_number = fields.Integer(allow_none=True)
    date_start = fields.Date(allow_none=True)
    date_end = fields.Date(allow_none=True)
    comment = fields.String(allow_none=True)
