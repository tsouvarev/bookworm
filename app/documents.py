import mongoengine
import pendulum


def _now():
    return pendulum.now('Europe/Moscow')


class Book(mongoengine.Document):
    author = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    pages_number = mongoengine.IntField(required=True)
    date_start = mongoengine.DateField(default=_now)
    date_end = mongoengine.DateField()
    comment = mongoengine.StringField()
    rating = mongoengine.IntField()
