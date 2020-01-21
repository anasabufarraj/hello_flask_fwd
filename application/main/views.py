# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from flask import render_template

from application.main import main


# ------------------------------------------------------------------------------
# Application Main Routing:
# ------------------------------------------------------------------------------
@main.route('/')
def index():
    return render_template('index.html')
