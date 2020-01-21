# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from urllib.parse import urlparse, urljoin

from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, fresh_login_required, current_user
from werkzeug.security import safe_str_cmp

from application import db
from application.auth import auth
from application.auth.forms import LoginForm, Registration, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
from application.email import send_email
from application.models import User


# ------------------------------------------------------------------------------
# Check for safe url
# ------------------------------------------------------------------------------
def is_safe_url(target):
    """Check if target URL is safe."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# ------------------------------------------------------------------------------
# Application Request Hooks
# ------------------------------------------------------------------------------
@auth.before_app_request
def before_request():
    """Returns unconfirmed template in case:
        1- If the user logged in.
        2- The account is not confirmed.
        3- The requested URL is outside of the authentication blueprint.
        4- The requested URL is not for a static file."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


# ------------------------------------------------------------------------------
# Application Authentication Routing:
# ------------------------------------------------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """loading the user from the database using the email provided with the form.
    If the password is valid, FlaskLogin’s login_user() function is invoked to record
    the user as logged in for the user session."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user=user, remember=form.remember_me.data)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('main.index'))
        flash('Invalid Username or Password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(subject='Confirm your account',
                   recipients=user.email,
                   template_name='auth/email/confirm',
                   user=user,
                   token=token)
        flash('A confirmation email has been sent to your inbox.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """Checks if the logged-in user is already confirmed, then redirects to the home page.
    When the confirmation succeeds, the User model’s confirmed attribute is changed and
    added to the session and then the database session is committed."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_generated_token(token):
        db.session.commit()
        flash('Thanks! You account has been confirmed.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """Generate and send new confirmation token by email."""
    token = current_user.generate_confirmation_token()
    send_email(subject='Confirm your account',
               recipients=current_user.email,
               template_name='auth/email/confirm',
               user=current_user,
               token=token)
    flash('A confirmation email has been resent to your inbox.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            if safe_str_cmp(form.old_password.data, form.new_password.data):
                flash('Cannot use old password.')
                return render_template("auth/change_password.html", form=form)
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        flash('Incorrect password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    elif form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(subject='Reset Your Password',
                       recipients=user.email,
                       template_name='auth/email/reset',
                       user=user,
                       token=token)
        flash('An email with instructions has been sent to your inbox.')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    elif form.validate_on_submit():
        if User.reset_password(token, form.new_password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
