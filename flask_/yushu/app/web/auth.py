from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from app.models.user import User
from . import web
from app.forms.auth_form import RegisterForm, LoginForm

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        redirect(url_for('web.login'))

    return render_template('auth/register.thml', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            logout_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswiith('/') :
                next = url_for('web.index')

            return render_template(next)
        else:
            flash('账号不存在或密码错误')

    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
