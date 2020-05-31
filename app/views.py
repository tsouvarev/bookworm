import os

from flask import Blueprint, render_template, request
from flask_httpauth import HTTPBasicAuth

from .documents import Book
from .forms import AddBoookForm

router = Blueprint(
    "router", __name__, template_folder="../templates", static_folder="../static"
)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    return username == os.environ["USER"] and password == os.environ["PASSWORD"]


@router.route("/", methods=["GET", "POST"])
@auth.login_required
def books():
    form = AddBoookForm()

    if request.method == "POST":
        if request.form.get("action") == "delete":
            Book.objects.get(id=request.form["id"]).delete()
        elif form.validate():
            Book(
                author=form.data["author"],
                title=form.data["title"],
                pages_number=form.data["pages_number"],
                date_start=form.data["date_start"],
                date_end=form.data["date_end"],
                comment=form.data["comment"],
            ).save()

    books = Book.objects.all()
    return render_template("reading_list.html", books=books, add_book_form=form)


@router.route("/stats")
@auth.login_required
def stats():
    total_pages_number = Book.objects.sum("pages_number")
    return render_template("stats.html", total_pages_number=total_pages_number)
