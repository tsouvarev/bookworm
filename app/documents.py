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
        # russian books might have english name,
        # but english books always have english author
        clean_author = re.sub(r'[^\w]', '', self.author)
        clean_title = re.sub(r'[^\w]', '', self.title)

        has_english_author = re.match('^[a-zA-Z0-9]+$', clean_author)
        has_english_title = re.match('^[a-zA-Z0-9]+$', clean_title)

        return bool(has_english_author and has_english_title)

    @property
    def is_helpful(self) -> bool:
        return self.rating and self.rating > MINIMAL_HELPFUL_RATING

    @property
    def days_reading(self) -> int:
        return (self.date_end - self.date_start).days
