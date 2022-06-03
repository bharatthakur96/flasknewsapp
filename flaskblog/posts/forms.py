from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flaskblog.models import CategoryEnum


class PostForm(FlaskForm):
    mychoices = [
        (CategoryEnum.task.value),
        (CategoryEnum.company.value),
        (CategoryEnum.hiring.value),
        (CategoryEnum.employee.value),
    ]
    category = SelectField("Category", choices=mychoices, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
