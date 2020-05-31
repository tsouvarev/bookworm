from datetime import datetime

import pendulum

SHORT_DATE_FORMAT = "%-d %b"
FULL_DATE_FORMAT = "%-d %b %Y"


def pretty_date(dt):
    today = datetime.today()
    if today.year == dt.year:
        return dt.strftime(SHORT_DATE_FORMAT)
    return dt.strftime(FULL_DATE_FORMAT)


def now():
    return pendulum.now("Europe/Moscow")
