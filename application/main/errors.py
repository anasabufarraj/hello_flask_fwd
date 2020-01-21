# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------
"""Application-wide errors handlers."""

from flask import render_template
from flask_wtf.csrf import CSRFError

from application.main import main


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', reason=error.description), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', reason=error.description), 500


@main.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html', reason=error.description), 400


@main.app_errorhandler(CSRFError)
def csrf_error(error):
    """Returns error template CSRF Error."""
    return render_template('errors/csrf_error.html', reason=error.description), 400
