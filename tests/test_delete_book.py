from http import HTTPStatus

from app.documents import Book


class TestDeleteBook:
    def test_delete(self, client, book):
        resp = client.delete(f'/books/{book.id}/')

        assert resp.status_code == HTTPStatus.OK
        assert Book.objects.filter(id=book.id).first() is None
