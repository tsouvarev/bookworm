from http import HTTPStatus

from pytest import mark

from app.documents import Book


class TestAddBook:
    data = {'author': 'some', 'title': 'another', 'pages_number': 111}

    def test_add_with_minimal_details(self, client):
        resp = client.post('/books/', json=self.data)

        assert resp.status_code == HTTPStatus.OK
        assert Book.objects.get(**self.data)

    @mark.parametrize(
        ('field', 'value'),
        [('date_end', '2024-01-01'), ('comment', 'some'), ('rating', 1)],
    )
    def test_add_with_optional_fields(self, client, field, value):
        data = self.data | {field: value}

        resp = client.post('/books/', json=data)

        assert resp.status_code == HTTPStatus.OK
        assert Book.objects.get(**data)
