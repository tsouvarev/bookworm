import re
from collections import defaultdict
from math import ceil

from funcy import group_by
from pendulum import Interval, interval
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
MINIMAL_HELPFUL_RATING = 3

monthly_stats_skeleton = lambda: defaultdict(
    lambda: defaultdict(lambda: defaultdict(int))
)
yearly_stats_skeleton = lambda: defaultdict(lambda: defaultdict(int))


def get_readable_month_name(month_number: int) -> str:
    return READABLE_MONTH_NAMES[month_number - 1]


def group_books(books: list[Book]) -> tuple[dict, dict, dict]:
    finished_books = filter(that.date_end, books)

    monthly_stats = monthly_stats_skeleton()
    english_stats = yearly_stats_skeleton()
    helpful_stats = yearly_stats_skeleton()
    total_stats = yearly_stats_skeleton()

    for book in finished_books:
        book_monthly_stats = _get_monthly_stats(book)
        _update_monthly_stats(monthly_stats, book_monthly_stats)

        book_yearly_stats = _get_yearly_stats(book)
        _update_yearly_stats(total_stats, book_yearly_stats)

        if re.match('^[a-zA-Z0-9]+$', re.sub(r'[^\w]', '', book.title)):
            _update_yearly_stats(english_stats, book_yearly_stats)

        if book.rating and book.rating > MINIMAL_HELPFUL_RATING:
            _update_yearly_stats(helpful_stats, book_yearly_stats)

    _update_total_stats(english_stats, total_stats)
    _update_total_stats(helpful_stats, total_stats)

    return {
        'monthly': monthly_stats,
        'total': total_stats,
        'english': english_stats,
        'helpful': helpful_stats,
    }


def _get_monthly_stats(book: Book) -> dict[tuple[int, int], int]:
    reading_time, pages_per_day = _get_book_stats(book)
    grouped_days = group_by(lambda d: (d.year, d.month), reading_time.range('days'))
    return {
        (year, month): ceil(pages_per_day * len(days))
        for (year, month), days in grouped_days.items()
    }


def _get_yearly_stats(book: Book) -> dict[int, int]:
    reading_time, pages_per_day = _get_book_stats(book)
    grouped_days = group_by(that.year, reading_time.range('days'))
    return {
        year: ceil(pages_per_day * len(days)) for year, days in grouped_days.items()
    }


def _update_monthly_stats(stats: dict, book_stats: dict[tuple[int, int], int]) -> None:
    for (year, month), pages in book_stats.items():
        s = stats[year][month]
        s['count'] += 1
        s['pages'] += pages


def _update_yearly_stats(stats: dict, book_yearly_stats: dict[int, int]) -> None:
    for year, pages in book_yearly_stats.items():
        s = stats[year]
        s['count'] += 1
        s['pages'] += pages


def _update_total_stats(stats: dict, total_stats: dict) -> None:
    for year in stats:
        stats[year]['percent'] = _get_percent(stats, total_stats, year, field='count')
        stats[year]['pages_percent'] = _get_percent(
            stats, total_stats, year, field='pages'
        )


def _get_book_stats(book: Book) -> tuple[Interval, float]:
    reading_time = interval(book.date_start, book.date_end)
    pages_per_day = book.pages_number / (reading_time.days + 1)
    return reading_time, pages_per_day


def _get_percent(stats: dict, total_stats: dict, year: int, field: str) -> int:
    return round(stats[year][field] / total_stats[year][field] * 100)
