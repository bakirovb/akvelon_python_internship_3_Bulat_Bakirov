from .models import *
from app import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction

    id = ma.auto_field()
    user_id = ma.auto_field()
    date = ma.auto_field()
    amount = ma.Float()


class NoUserIdTransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction

    id = ma.auto_field()
    date = ma.auto_field()
    amount = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

tx_schema = TransactionSchema()
txs_schema = TransactionSchema(many=True)

no_user_id_tx_schema = NoUserIdTransactionSchema()
no_user_id_txs_schema = NoUserIdTransactionSchema(many=True)