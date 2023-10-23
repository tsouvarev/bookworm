import re
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import groupby
from typing import Optional

from whatever import that

from .documents import Book

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
class BooksStats:
    books: list
    total_stats: Optional['BooksStats'] = None

    @property
    def count(self):
        return len(self.books)

    @property
    def percent(self):
        if self.total_stats is None:
            raise NotImplementedError
        return round(self.count / self.total_stats.count * 100)

    @property
    def pages(self):
        return sum(book.pages_number for book in self.books)

    @property
    def pages_percent(self):
        if self.total_stats is None:
            raise NotImplementedError
        return round(self.pages / self.total_stats.pages * 100)


@dataclass
class BooksByMonth:
    month: int
    stats: BooksStats


@dataclass
class BooksByYear:
    year: int
    books: list[Book]

    @property
    def books_by_month(self) -> Iterable[BooksByMonth]:
        grouped_by_month = groupby(self.books, that.date_start.month)
        for month, books in grouped_by_month:
            yield BooksByMonth(month, BooksStats(list(books)))

    @property
    def stats(self):
        return BooksStats(self.books)

    @property
    def helpful_stats(self):
        minimal_helpful_rating = 3
        helpful_books = [
            book
            for book in self.books
            if book.rating and book.rating > minimal_helpful_rating
        ]
        return BooksStats(helpful_books, total_stats=self.stats)

    @property
    def english_stats(self):
        english_books = [
            book
            for book in self.books
            if re.match('^[a-zA-Z0-9]+$', re.sub(r'[^\w]', '', book.title))
        ]
        return BooksStats(english_books, total_stats=self.stats)


def get_readable_month_name(month_number):
    return READABLE_MONTH_NAMES[month_number - 1]


def group_books(books: list[Book]) -> Iterable[BooksByYear]:
    grouped_by_year = groupby(books, that.date_start.year)
    for year, books in grouped_by_year:
        yield BooksByYear(year, list(books))
