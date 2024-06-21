from datetime import datetime
from functools import partial

from app.utils import BooksByMonth, BooksByYear, BooksStats, group_books
from tests.factories import BookFactory


class TestGroupBooks:
    _create_book = partial(BookFactory.create, with_date_end=True)

    def test_skips_books_without_date_end(self):
        book = BookFactory.create(with_date_start=True)
        grouped = group_books([book])
        assert list(grouped) == []

    def test_groups_by_year(self):
        book_2021 = self._create_book(date_start=_dt(2021))
        book_2022 = self._create_book(date_start=_dt(2022))

        grouped = group_books([book_2021, book_2022])

        assert list(grouped) == [
            BooksByYear(2021, [book_2021]),
            BooksByYear(2022, [book_2022]),
        ]

    def test_groups_by_month(self):
        book_2 = self._create_book(date_start=_dt(month=2))
        book_3 = self._create_book(date_start=_dt(month=3))

        grouped = group_books([book_2, book_3])

        assert list(list(grouped)[0].books_by_month) == [
            BooksByMonth(2, BooksStats([book_2])),
            BooksByMonth(3, BooksStats([book_3])),
        ]


def _dt(year=2024, month=2):
    return datetime(year, month, 2)
