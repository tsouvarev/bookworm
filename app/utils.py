from calendar import month_name

import pendulum


def now():
    return pendulum.now("Europe/Moscow")


def get_readable_month_name(month_number):
    return month_name[month_number]
