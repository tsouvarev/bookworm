import os
from base64 import b64encode
from http import HTTPStatus

from flask import Blueprint, current_app, render_template, request
from flask_httpauth import HTTPBasicAuth
from pydantic import ValidationError

from .documents import Book
from .schemes import AddBookSchema, BookSchema, EditBookSchema
from .utils import generate_scatter, get_error_messages, group_books, model_dump

router = Blueprint(
    'router', __name__, template_folder='../templates', static_folder='../static'
)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if current_app.config['TESTING']:
        return True
    return username == os.environ['USER'] and password == os.environ['PASSWORD']


@router.route('/', methods=['GET'])
@auth.login_required
def start():
    return render_template('start.html')


@router.route('/books/', methods=['GET'])
@auth.login_required
def books_list():
    books = Book.objects.order_by('-date_start')
    books_with_unfinished_first = sorted(books, key=lambda b: b.date_end is not None)

    return model_dump(BookSchema, books_with_unfinished_first, many=True)


@router.route('/books/', methods=['POST'])
@auth.login_required
def add_book():
    try:
        data = AddBookSchema(**request.json).model_dump()
    except ValidationError as err:
        return {'errors': get_error_messages(err)}, HTTPStatus.BAD_REQUEST

    book = Book(**data).save()

    return model_dump(BookSchema, book)


@router.route('/books/<book_id>/', methods=['PATCH'])
@auth.login_required
def edit_book(book_id):
    try:
        data = EditBookSchema(**request.json).model_dump()
    except ValidationError as err:
        return {'errors': get_error_messages(err)}, HTTPStatus.BAD_REQUEST

    Book.objects.filter(id=book_id).update(**data)

    return {}


@router.route('/books/<book_id>/', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    Book.objects.filter(id=book_id).delete()
    return {}


@router.route('/stats')
@auth.login_required
def stats():
    books = Book.objects.order_by('-date_start')
    scatter = b64encode(generate_scatter(books)).decode()

    context = {'scatter': (scatter), **group_books(books)}
    return render_template('stats.html', **context)
