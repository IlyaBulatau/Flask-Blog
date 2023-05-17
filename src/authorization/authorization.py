from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, current_user, login_user, logout_user

from authorization import forms
from database import models
from log.log import log

authorization = Blueprint('authorization', __name__, template_folder='templates')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@authorization.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обработчик страницы авторизации пользователей
    """
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            remember = True if form.is_remember.data else False

            user = models.db.session.query(models.User).filter(models.User.email == email).first()
            login_user(user, remember=remember)
            return redirect(url_for('index'))

    return render_template('authorization/login.html', form=form)

@authorization.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Обработчик страницы регистрации пользователей
    """
    form = forms.SingupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            user = models.User(username=username, email=email, password=password)
            models.db.session.add(user)
            models.db.session.commit()
            
            return redirect(url_for('.login'))
    return render_template('authorization/signup.html', form=form)

@authorization.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))