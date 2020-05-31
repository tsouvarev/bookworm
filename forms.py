import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import data_required, optional


class AddBoookForm(FlaskForm):
    author = wtforms.StringField(label="Автор", validators=[data_required()])
    title = wtforms.StringField(label="Название", validators=[data_required()])
    pages_number = wtforms.IntegerField(
        label="Число страниц", validators=[data_required()]
    )
    date_start = wtforms.DateField(label="Дата начала чтения", validators=[optional()])
    date_end = wtforms.DateField(label="Дата окончания чтения", validators=[optional()])
    comment = wtforms.StringField(label="Комментарий", validators=[optional()])
