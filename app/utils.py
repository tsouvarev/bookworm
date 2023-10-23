from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import starmap

import pendulum

READABLE_MONTH_NAMES = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
]


@dataclass
class GroupedBooks:
    month: int
    data: list

    @property
    def pages_sum(self):
        return sum(book.pages_number for book in self.data)

    @property
    def books_number(self):
        return len(self.data)


def now():
    return pendulum.now('Europe/Moscow')


def get_readable_month_name(month_number):
    return READABLE_MONTH_NAMES[month_number - 1]


def group_books(books):
    grouped = defaultdict(lambda: defaultdict(list))
    for book in books:
        grouped[book.date_start.year][book.date_start.month].append(book)

    for year, grouped_by_month in grouped.items():
        aggregated_books = list(_aggregate_books(grouped_by_month))
        yield year, aggregated_books


def _aggregate_books(grouped_by_month: dict[int, list]) -> Iterable[GroupedBooks]:
    yield from starmap(GroupedBooks, grouped_by_month.items())
