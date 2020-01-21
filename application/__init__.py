# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------
"""Application factory and main Blueprint registration."""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Login required.'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = 'Please reauthenticate.'
login_manager.needs_refresh_message_category = 'warning'


def create_app(config_name):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # --------------------------------------------------------------------------
    # Main Blueprint Registration:
    # --------------------------------------------------------------------------
    from application.main import main, views, errors
    from application.auth import auth, views

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    return app
