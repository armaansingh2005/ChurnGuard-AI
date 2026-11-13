from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, PasswordField, StringField, validators

from app import db
from app.models.database_models import User

auth_bp = Blueprint("auth", __name__)


class LoginForm(Form):
    username = StringField("Username", [validators.InputRequired(), validators.Length(min=3, max=80)])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=6)])

    def csrf_token(self):
        return None


class RegisterForm(Form):
    username = StringField("Username", [validators.InputRequired(), validators.Length(min=3, max=80)])
    email = StringField("Email", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=6)])

    def csrf_token(self):
        return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard.dashboard_page"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists.", "warning")
        elif User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "warning")
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
