from flask import (
    Blueprint, request, jsonify
)

from datetime import datetime, timedelta
from .models import Transaction
from app import db
from sqlalchemy import func

bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.route('', methods=['GET'])
def expense_income_statistics():
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date or end_date:
        if not start_date:
            start_date = datetime.fromordinal(0)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if not end_date:
            end_date = start_date + timedelta(days=1)
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

    txs = db.session.query(func.date(Transaction.date), func.sum(Transaction.amount)). \
        filter_by(user_id=user_id)
    if start_date:
        txs = txs.filter(Transaction.date.between(start_date, end_date))

    txs = txs.group_by(func.date(Transaction.date))

    txs = txs.all()

    total_sum = 0
    data = []
    for row in txs:
        data.append({'date': row[0], 'sum': row[1] / 100})
        total_sum += row[1]/100

    return jsonify(start_date=start_date, end_date=end_date, data=data, total_sum=total_sum)
