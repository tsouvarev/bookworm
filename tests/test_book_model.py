from pytest import mark

from tests.factories import BookFactory


class TestBookModel:
    @mark.parametrize(
        ('title', 'author', 'is_english'),
        [
            ('eng title', 'eng author', True),
            ('eng title', 'русский автор', False),
            ('русское название', 'eng author', False),
            ('русское название', 'русский автор', False),
        ],
    )
    def test_is_english(self, title, author, is_english):
        book = BookFactory.create(title=title, author=author)
        assert book.is_english is is_english
