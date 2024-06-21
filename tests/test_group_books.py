from datetime import datetime
from functools import partial

from app.utils import group_books
from tests.factories import BookFactory


class TestGroupBooks:
    _create_book = partial(BookFactory.create, with_date_end=True)

    def test_monthly_skips_books_without_date_end(self):
        book = BookFactory.create(with_date_start=True)
        assert group_books([book])['monthly'] == {}

    def test_groups_by_year(self):
        book_2021 = self._create_book(date_start=_dt(2021))
        book_2022 = self._create_book(date_start=_dt(2022))

        grouped = group_books([book_2021, book_2022])

        assert grouped['monthly'] == {
            2021: {2: {'count': 1, 'pages': 1}},
            2022: {2: {'count': 1, 'pages': 1}},
        }

    def test_groups_by_month(self):
        book_2 = self._create_book(date_start=_dt(month=2))
        book_3 = self._create_book(date_start=_dt(month=3))

        grouped = group_books([book_2, book_3])

        assert grouped['monthly'] == {
            2024: {2: {'count': 1, 'pages': 1}, 3: {'count': 1, 'pages': 1}}
        }

    def test_groups_english(self):
        book_eng = self._create_book(date_start=_dt(), title='some')
        book_other = self._create_book(date_start=_dt(), title='книга')

        grouped = group_books([book_eng, book_other])

        assert grouped['english'] == {
            2024: {'count': 1, 'pages': 1, 'percent': 50, 'pages_percent': 50}
        }

    def test_groups_helpful(self):
        book_helpless = self._create_book(date_start=_dt(), rating=1)
        book_helpful = self._create_book(date_start=_dt(), rating=4)

        grouped = group_books([book_helpless, book_helpful])

        assert grouped['helpful'] == {
            2024: {'count': 1, 'pages': 1, 'percent': 50, 'pages_percent': 50}
        }

    def test_groups_total(self):
        book_helpless = self._create_book(date_start=_dt())
        book_helpful = self._create_book(date_start=_dt())

        grouped = group_books([book_helpless, book_helpful])

        assert grouped['total'] == {2024: {'count': 2, 'pages': 2}}


def _dt(year=2024, month=2):
    return datetime(year, month, 2)
