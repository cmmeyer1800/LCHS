from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # filename = db.Column(db.String(), unique=True)
    title = db.Column(db.String(512), unique=True)
    length = db.Column(db.Float)
    genre = db.Column(db.String(100))
    actors = db.Column(db.String(1024))
    keywords = db.Column(db.String(1024))


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(512), unique=True)
    keywords = db.Column(db.String(1024))
    date = db.Column(db.DateTime)
    people = db.Column(db.String(1024))