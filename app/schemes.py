from datetime import date

from marshmallow import Schema, fields
from pendulum import now

from app.documents import Book


class BookSchema(Schema):
    id = fields.String()
    author = fields.String()
    title = fields.String()
    pages_number = fields.Integer()
    date_start = fields.Method('get_date_start')
    date_end = fields.Method('get_date_end')
    comment = fields.String()
    rating = fields.Integer()

    def get_date_start(self, book: Book) -> str:
        return self._format_date(book.date_start)

    def get_date_end(self, book: Book) -> str | None:
        if not book.date_end:
            return None
        return self._format_date(book.date_end)

    def _format_date(self, d: date) -> str:
        if d.year == now().year:
            return d.strftime('%-d %b')
        return d.strftime('%-d %b %Y')


class AddBoookSchema(Schema):
    author = fields.String(required=True)
    title = fields.String(required=True)
    pages_number = fields.Integer(required=True)
    date_start = fields.Date()
    date_end = fields.Date()
    comment = fields.String()
    rating = fields.Integer()


class EditBoookSchema(Schema):
    author = fields.String(allow_none=True)
    title = fields.String(allow_none=True)
    pages_number = fields.Integer(allow_none=True)
    date_start = fields.Date(allow_none=True)
    date_end = fields.Date(allow_none=True)
    comment = fields.String(allow_none=True)
    rating = fields.Integer(allow_none=True)
