from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update(
    SECRET_KEY='bf9d247b9d724be9858ca84d326cb77c',
    SQLALCHEMY_DATABASE_URI="mysql://root:@localhost/sqlalchemy",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    balance = db.Column(db.Integer)
    password = db.Column(db.String(80))

    def __init__(self, username, email, balance, password):
        self.username = username
        self.email = email
        self.balance = balance
        self.password = password
