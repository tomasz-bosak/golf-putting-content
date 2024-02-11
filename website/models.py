from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     data = db.Column(db.String(10000))
     date = db.Column(db.DateTime(timezone=True), default=func.now())
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Game(db.Model):
     id = db.Column (db.Integer, primary_key = True)
     host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     guest_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     host_score = db.Column(db.Float)
     guest_score = db.Column(db.Float)
     accepted = db.Column(db.Boolean)

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(150), unique=True)
     password = db.Column(db.String(150))
     first_name = db.Column(db.String(150))
     index = db.Column(db.Float)
     game_host = db.relationship('Game', foreign_keys='Game.host_id')
     game_guest = db.relationship('Game', foreign_keys='Game.guest_id')
     notes = db.relationship('Note')
