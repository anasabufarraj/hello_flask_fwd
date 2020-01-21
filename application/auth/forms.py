# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from application.models import User


# ------------------------------------------------------------------------------
# Application Authentication WTForms Setup:
# ------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    """User Login WTForms."""
    email = StringField(
        'Email', validators=[DataRequired('Email address is required'),
                             Length(1, 64),
                             Email('Invalid email address')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class Registration(FlaskForm):
    """User Registration WTForms."""
    email = StringField('Email', validators=[DataRequired('Email address is required'), Length(1, 64)])
    username = StringField('Username',
                           validators=[
                               DataRequired('Username is required'),
                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                      'Username must have only letters, numbers, dots or underscores')
                           ])
    password = PasswordField(
        'Password',
        validators=[DataRequired('Password is required'),
                    EqualTo('password_confirm', 'Password must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired('Password confirmation required')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Custom validation method invoked in addition to email field defined validators.
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        """Custom validation method invoked in addition to username field defined validators.
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already used')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(),
                                             EqualTo('password_confirm', 'Password must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(),
                                             EqualTo('password_confirm', 'Password must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
