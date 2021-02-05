from calendar import month_name
from collections import defaultdict
from dataclasses import dataclass
from itertools import starmap
from typing import Dict, Iterable

import pendulum


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
    return pendulum.now("Europe/Moscow")


def get_readable_month_name(month_number):
    return month_name[month_number]


def group_books(books):
    grouped = defaultdict(lambda: defaultdict(list))
    for book in books:
        grouped[book.date_start.year][book.date_start.month].append(book)

    for year, grouped_by_month in grouped.items():
        aggregated_books = list(_aggregate_books(grouped_by_month))
        yield year, aggregated_books


def _aggregate_books(grouped_by_month: Dict[int, list]) -> Iterable[GroupedBooks]:
    yield from starmap(GroupedBooks, grouped_by_month.items())
