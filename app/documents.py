import re

import mongoengine

MINIMAL_HELPFUL_RATING = 3


class Book(mongoengine.Document):
    author = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    pages_number = mongoengine.IntField(required=True)
    date_start = mongoengine.DateField()
    date_end = mongoengine.DateField()
    comment = mongoengine.StringField()
    rating = mongoengine.IntField()

    @property
    def is_english(self) -> bool:
        clean_title = re.sub(r'[^\w]', '', self.title)
        return bool(re.match('^[a-zA-Z0-9]+$', clean_title))

    @property
    def is_helpful(self) -> bool:
        return self.rating and self.rating > MINIMAL_HELPFUL_RATING

    @property
    def days_reading(self) -> int:
        return (self.date_end - self.date_start).days
