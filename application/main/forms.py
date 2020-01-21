# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# ------------------------------------------------------------------------------
# Application Main WTForms Setup:
# -----------------------------------------------------------------------------
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired('Username is required!')])
    submit = SubmitField('Submit')
