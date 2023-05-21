from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_ckeditor import CKEditorField
from wtforms.validators import ValidationError

from blog.redis import redis
from flask_login import current_user
from log.log import log
from database import models


class ValidatorTitle:
    """
    Валидотор заголовков постов
    Дл того что бы названия постов были уникальными
    """
    def __call__(self, form, field):
        if models.db.session.query(models.Post).filter(models.Post.title == field.data).first():
            raise ValidationError('This title have in DB')


class ValidatorLimitAddPost:
    """
    Валидатор ограничени публикации постов для кнопки на страницы создания поста
    Ищет в кэше редис ключ с ид юзера и если такой ключ есть то запрещает публикацию
    """

    def __call__(self, form, field):
        if redis.get(current_user.id):
            raise ValidationError('Posting limit 1 per day')

class PostAddForm(FlaskForm):
    title = StringField(label='Title', validators=[InputRequired(), Length(min=8, max=100), ValidatorTitle()])
    text = TextAreaField(label='Content', validators=[InputRequired(), Length(min=255)])
    submit = SubmitField(validators=[ValidatorLimitAddPost()])

class PostChangeForm(FlaskForm):
    text = CKEditorField(label='Change text this post', validators=[Length(min=255)])
    save = SubmitField('Save') 
    cancel = SubmitField('Cancel')