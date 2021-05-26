from app import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    transactions = db.relationship('Transaction', backref='users')


class Transaction(db.Model):
    __tablename__ = 'transactions_info'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.BigInteger(), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime(), server_default=func.now(), nullable=False)
