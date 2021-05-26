from flask import (
    Blueprint, request, jsonify
)

from datetime import datetime, timedelta
from sqlalchemy import desc

from .models import Transaction, User
from .serializers import tx_schema, txs_schema
from app import db

bp = Blueprint('transactions', __name__, url_prefix='/tx')


@bp.route('', methods=['GET'])
def all_transactions():
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tx_type = request.args.get('tx_type')
    by_date = request.args.get('by_date')
    by_amount = request.args.get('by_amount')

    if not user_id:
        txs = db.session.query(Transaction)
        return jsonify(items=txs_schema.dump(txs))

    if start_date or end_date:
        if not start_date:
            start_date = datetime.fromordinal(0)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if not end_date:
            end_date = start_date + timedelta(days=1)
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

    txs = db.session.query(Transaction.id, Transaction.amount, Transaction.date)
    if start_date:
        txs = txs.filter(Transaction.date.between(start_date, end_date))
    if tx_type == '0':
        txs = txs.filter(Transaction.amount < 0)
    if tx_type == '1':
        txs = txs.filter(Transaction.amount > 0)

    if by_date == '1':
        txs = txs.order_by(Transaction.date)
    if by_date == '0':
        txs = txs.order_by(Transaction.date.desc())
    if by_amount == '1':
        txs = txs.order_by(Transaction.amount)
    if by_amount == '0':
        txs = txs.order_by(Transaction.amount.desc())
    txs = txs.all()

    return jsonify(items=txs_schema.dump(txs))


@bp.route('', methods=['POST'])
def create_transaction():
    user_id = request.args.get('user_id')
    if not db.session.query(User).get(user_id):
        return jsonify(resultCode=1, messages=[], data={})

    tx = Transaction(amount=request.form.get('amount'), user_id=user_id)
    db.session.add(tx)
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})


@bp.route('/<int:tx_id>', methods=['GET'])
def transaction_info_by_id(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx:
        return jsonify(resultCode=1, messages=[], data={})

    return tx_schema.dump(tx)


@bp.route('/<int:tx_id>', methods=['DELETE'])
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id)
    if not tx.count():
        return jsonify(resultCode=1, messages=[], data={})
    tx.delete()
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})


@bp.route('/<int:tx_id>', methods=['PUT'])
def update_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id)
    if not tx.count():
        return jsonify(resultCode=1, messages=[], data={})
    tx.update(request.form)
    db.session.commit()

    return jsonify(resultCode=0, messages=[], data={})
