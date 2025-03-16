from http import HTTPStatus

import pendulum

from .factories import BookFactory
from .utils import as_json


class TestGetBooks:
    def test_get_list_partial_details(self, client):
        books = BookFactory.create_batch(size=3)

        resp = client.get('/books/')

        assert resp.status_code == HTTPStatus.OK
        assert as_json(resp) == _serialize_books(books)

    def test_get_list_full_details(self, client):
        now = pendulum.now().date()
        books = BookFactory.create_batch(size=3, date_end=now, comment='some', rating=2)

        resp = client.get('/books/')

        assert resp.status_code == HTTPStatus.OK
        assert as_json(resp) == _serialize_books(
            books, date_end=now.isoformat(), comment='some', rating=2
        )


def _serialize_books(books, **extra):
    return [_serialize_book(book, **extra) for book in books]


def _serialize_book(book, **extra):
    return {
        'id': str(book.id),
        'author': book.author,
        'title': book.title,
        'pages_number': book.pages_number,
        'date_start': None,
        'date_end': None,
        'comment': None,
        'rating': None,
    } | extra
