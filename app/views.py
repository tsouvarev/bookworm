import os
from http import HTTPStatus

from flask import Blueprint, current_app, render_template, request
from flask_httpauth import HTTPBasicAuth
from marshmallow import ValidationError

from .documents import Book
from .schemes import AddBoookSchema, BookSchema, EditBoookSchema
from .utils import group_books

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
    return BookSchema().dumps(books, many=True)


@router.route('/books/', methods=['POST'])
@auth.login_required
def add_book():
    try:
        data = AddBoookSchema().load(request.json)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    book = Book(**data).save()
    return BookSchema().dumps(book)


@router.route('/books/<book_id>/', methods=['PATCH'])
@auth.login_required
def edit_book(book_id):
    try:
        data = EditBoookSchema().load(request.json)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
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
    return render_template('stats.html', grouped=group_books(books))
