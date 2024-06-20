from http import HTTPStatus

import pendulum
from pytest import mark

from app.documents import Book


class TestEditBook:
    data = {'author': 'some', 'title': 'another', 'pages_number': 111}

    @mark.parametrize(
        ('field', 'value'),
        [
            ('author', 'another'),
            ('title', 'wow'),
            ('pages_number', 222),
            ('comment', 'some'),
            ('rating', 1),
        ],
    )
    def test_edit_simple(self, client, book, field, value):
        data = self.data | {field: value}

        resp = client.patch(f'/books/{book.id}/', json=data)

        book = _refresh_from_db(book)
        assert resp.status_code == HTTPStatus.OK
        assert getattr(book, field) == value

    @mark.parametrize(
        ('field', 'value'), [('date_start', '2024-01-01'), ('date_end', '2024-01-01')]
    )
    def test_edit_dates(self, client, book, field, value):
        data = self.data | {field: value}

        resp = client.patch(f'/books/{book.id}/', json=data)

        book = _refresh_from_db(book)
        assert resp.status_code == HTTPStatus.OK
        assert getattr(book, field) == pendulum.parse(value).date()


def _refresh_from_db(book):
    return Book.objects.get(id=book.id)
