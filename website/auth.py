from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/logIn', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password, Try Again!", category="error")
        else:
            flash("User does not exist.", category="error")

    return render_template("logIn.html")


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))


@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        fullName = request.form.get("fullName")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email Already Exist.", category='error')
        elif len(fullName) < 5:
            flash("Enter Full Name", category='error')
        elif len(email) < 4:
            flash("Email Not Valid.", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match.", category='error')
        elif len(password1) < 5:
            flash("Password must be atleast 5 character.", category='error')
        else:
            new_user = User(email=email, fullName=fullName, password=generate_password_hash(
                password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signUp.html")
