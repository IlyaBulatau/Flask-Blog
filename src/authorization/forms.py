from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import Length, InputRequired, Email, EqualTo, ValidationError

from database import models
from log.log import log


class ValidatorEmailUnique:
    """
    Валидатор email для формы регистрации
    проверяет уникальность email в БД 
    """

    def __call__(self, form, field):
        """
        form: Форма
        field: Поле формы
        """
        if models.db.session.query(models.User).filter(models.User.email == field.data).first():
            raise ValidationError('This Email exists')
        
class ValidatorLoginUser:
    """
    Валидатор для формы авторизации
    Сначала идет проверка какое это поле email/password
    Далее email проверяется на присутствие в Бд
    password на совпадение с паролем юзера из БД, который ищется по email полю(См. метод is_valid_password)
    """

    def __call__(self, form, field):
        """
        form: Форма
        field: Поле формы
        """
        if field.name == 'email':
            email = models.db.session.query(models.User).filter(models.User.email == field.data).first()
            if not email:
                raise ValidationError('This Email not register')
            
        if field.name == 'password':
            self.is_valid_password(form, field.data)

    @staticmethod
    def is_valid_password(form, password):
        email_in_form = form.email.data
        user = models.db.session.query(models.User).filter(models.User.email == email_in_form).first()
        if not user:
            raise ValidationError()
        if user.password != password:
            raise ValidationError('Incorrect password')
        


class LoginForm(FlaskForm):
    email = EmailField(label='E-mail', validators=[Email(), InputRequired(), ValidatorLoginUser()])
    password = PasswordField(label='Password', validators=[InputRequired(), ValidatorLoginUser()])
    submit = SubmitField()
    is_remember = BooleanField(label='Remember?')


class SingupForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=3, max=20), InputRequired()])
    email = EmailField(label='E-mail', validators=[Email(), InputRequired(), ValidatorEmailUnique()])
    password = PasswordField(label='Password', validators=[InputRequired()])
    password2 = PasswordField(label='Password Again', validators=[EqualTo(fieldname='password'), InputRequired()])
    submit = SubmitField()




