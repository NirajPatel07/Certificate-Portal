from flask import Blueprint
from flask.templating import render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def signUp():
  return render_template("signUp.html")

@views.route('/home')
@login_required
def home():
  return render_template("index.html", user=current_user)

@views.route('/createCertificate')
def createCertificate():
  return render_template("createCertificate.html")

@views.route('/verifyCertificate')
def verifyCertificate():
  return render_template("verifyCertificate.html")

@views.route('/csvCertificate')
def csvCertificate():
  return render_template("upload.html")

@views.route('/about')
def about():
  return render_template("about.html")