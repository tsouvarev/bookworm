import factory

from app.documents import Book


class MongoEngineFactory(factory.Factory):
    """Factory for mongoengine objects."""

    class Meta:
        abstract = True

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = model_class(*args, **kwargs)
        if instance._is_document:
            instance.save()
        return instance


class BookFactory(MongoEngineFactory):
    author = factory.Faker('name')
    title = factory.Faker('catch_phrase')
    pages_number = factory.Faker('pyint')

    class Meta:
        model = Book

    class Params:
        with_date_end = factory.Trait(date_end=factory.Faker('date'))
        with_date_start = factory.Trait(date_start=factory.Faker('date'))
