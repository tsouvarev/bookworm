import re
from collections import defaultdict

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


def get_readable_month_name(month_number):
    return READABLE_MONTH_NAMES[month_number - 1]


def group_books(books: list[Book]) -> tuple[dict, dict, dict]:
    finished_books = filter(that.date_end, books)

    monthly_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    english_stats = defaultdict(lambda: defaultdict(int))
    helpful_stats = defaultdict(lambda: defaultdict(int))
    total_stats = defaultdict(lambda: defaultdict(int))

    for book in finished_books:
        _update_stats(monthly_stats, book, use_month=True)
        _update_stats(total_stats, book)

        if re.match('^[a-zA-Z0-9]+$', re.sub(r'[^\w]', '', book.title)):
            _update_stats(english_stats, book)

        if book.rating and book.rating > MINIMAL_HELPFUL_RATING:
            _update_stats(helpful_stats, book)

    _update_total_stats(english_stats, total_stats)
    _update_total_stats(helpful_stats, total_stats)

    return {
        'monthly': monthly_stats,
        'total': total_stats,
        'english': english_stats,
        'helpful': helpful_stats,
    }


def _update_stats(stats, book, *, use_month=False):
    s = stats[book.date_start.year]
    if use_month:
        s = s[book.date_start.month]

    s['count'] += 1
    s['pages'] += book.pages_number


def _update_total_stats(stats, total_stats):
    for year in stats:
        stats[year]['percent'] = _get_percent(stats, total_stats, year, field='count')
        stats[year]['pages_percent'] = _get_percent(
            stats, total_stats, year, field='pages'
        )


def _get_percent(stats, total_stats, year, field):
    return round(stats[year][field] / total_stats[year][field] * 100)
