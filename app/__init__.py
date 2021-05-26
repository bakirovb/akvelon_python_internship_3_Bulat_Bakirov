from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from dotenv import load_dotenv

db = SQLAlchemy()
ma = Marshmallow()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_mapping(test_config)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)
    ma.init_app(app)

    from . import user, transaction, statistic
    app.register_blueprint(user.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(statistic.bp)

    load_dotenv()

    return app
