from flask import (
    Blueprint, request, jsonify
)

from .models import User
from .serializers import user_schema, users_schema
from app import db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def all_users():
    by_name = request.args.get('by_name')

    user = User.query
    if by_name == '1':
        user = user.order_by(User.first_name, User.last_name)
    if by_name == '0':
        user = user.order_by(User.first_name.desc(), User.last_name.desc())
    users = user.all()

    return jsonify(items=users_schema.dump(users))


@bp.route('/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(resultCode=1, messages=[], data={})

    return user_schema.dump(user)


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id)
    if not user.count():
        return jsonify(resultCode=1, messages=[], data={})
    user.delete()
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})


@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id)
    if not user.count():
        return jsonify(resultCode=1, messages=[], data={})
    user.update(request.form)
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})


@bp.route('', methods=['POST'])
def create_user():
    user = User(first_name=request.form['first_name'], last_name=request.form['last_name'],
                email=request.form['email'])
    db.session.add(user)
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})
