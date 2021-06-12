from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email=db.Column(db.String(150), unique=True)
  password=db.Column(db.String(150))
  fullName=db.Column(db.String(150))
  
class block_chain_data(db.Model):
  blockHash= db.Column(db.String(250), primary_key=True)
  fullName=db.Column(db.String(150))
  clgName=db.Column(db.String(250))
  
  
