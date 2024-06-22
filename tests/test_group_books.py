from datetime import datetime
from functools import partial

from app.utils import group_books
from tests.factories import BookFactory


class TestGroupBooks:
    _create_book = partial(BookFactory.create, with_date_end=True)

    def test_monthly_skips_books_without_date_end(self):
        book = BookFactory.create(with_date_start=True)
        assert group_books([book])['monthly'] == {}

    def test_groups_by_month(self):
        book_2 = self._create_book(date_start=_dt(month=2), date_end=_dt(month=4))
        book_3 = self._create_book(date_start=_dt(month=3), date_end=_dt(month=5))

        grouped = group_books([book_2, book_3])

        assert grouped['monthly'] == {
            2024: {
                2: {'count': 1, 'pages': 1},
                3: {'count': 2, 'pages': 2},
                4: {'count': 2, 'pages': 2},
                5: {'count': 1, 'pages': 1},
            }
        }

    def test_groups_by_month_overflow(self):
        book = self._create_book(date_start=_dt(2021), date_end=_dt(2022))

        grouped = group_books([book])

        assert grouped['monthly'] == {
            2021: dict.fromkeys(range(2, 13), {'count': 1, 'pages': 1}),
            2022: dict.fromkeys(range(1, 3), {'count': 1, 'pages': 1}),
        }

    def test_groups_english(self):
        book_eng = self._create_book(date_start=_dt(), date_end=_dt(), title='some')
        book_other = self._create_book(date_start=_dt(), date_end=_dt(), title='книга')

        grouped = group_books([book_eng, book_other])

        assert grouped['english'] == {
            2024: {'count': 1, 'pages': 1, 'percent': 50, 'pages_percent': 50}
        }

    def test_groups_english_overflow(self):
        book = self._create_book(date_start=_dt(2021), date_end=_dt(2022), title='some')

        grouped = group_books([book])

        assert grouped['english'] == {
            2021: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
            2022: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
        }

    def test_groups_helpful(self):
        book_helpless = self._create_book(date_start=_dt(), date_end=_dt(), rating=1)
        book_helpful = self._create_book(date_start=_dt(), date_end=_dt(), rating=4)

        grouped = group_books([book_helpless, book_helpful])

        assert grouped['helpful'] == {
            2024: {'count': 1, 'pages': 1, 'percent': 50, 'pages_percent': 50}
        }

    def test_groups_helpful_overflow(self):
        book = self._create_book(date_start=_dt(2021), date_end=_dt(2022), rating=4)

        grouped = group_books([book])

        assert grouped['english'] == {
            2021: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
            2022: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
        }

    def test_groups_total(self):
        book_helpless = self._create_book(date_start=_dt(), date_end=_dt())
        book_helpful = self._create_book(date_start=_dt(), date_end=_dt())

        grouped = group_books([book_helpless, book_helpful])

        assert grouped['total'] == {2024: {'count': 2, 'pages': 2}}

    def test_groups_total_overflow(self):
        book = self._create_book(date_start=_dt(2021), date_end=_dt(2022))

        grouped = group_books([book])

        assert grouped['english'] == {
            2021: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
            2022: {'count': 1, 'pages': 1, 'percent': 100, 'pages_percent': 100},
        }


def _dt(year=2024, month=2):
    return datetime(year, month, 2)
