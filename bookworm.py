import os

import mongoengine
from dotenv import load_dotenv
from flask import (Flask, render_template, request,
                   send_from_directory)
from flask_httpauth import HTTPBasicAuth

from documents import Book
from forms import AddBoookForm
from utils import pretty_date

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.template_filter()(pretty_date)

auth = HTTPBasicAuth()
mongoengine.connect(host=os.environ['MONGO_URI'])


@auth.verify_password
def verify_password(username, password):
    return username == os.environ['USER'] and password == os.environ['PASSWORD']


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def books():
    form = AddBoookForm()

    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            Book.objects.get(id=request.form['id']).delete()
        elif form.validate():
            Book(
                author=form.data['author'],
                title=form.data['title'],
                pages_number=form.data['pages_number'],
                date_start=form.data['date_start'],
                date_end=form.data['date_end'],
                comment=form.data['comment'],
            ).save()

    books = Book.objects.all()
    return render_template('reading_list.html', books=books, add_book_form=form)


@app.route('/stats')
@auth.login_required
def stats():
    total_pages_number = Book.objects.sum('pages_number')
    return render_template('stats.html', total_pages_number=total_pages_number)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
