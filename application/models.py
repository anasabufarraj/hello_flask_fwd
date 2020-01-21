# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from application import login_manager


# ------------------------------------------------------------------------------
# SQLAlchemy Database Models Setup (SQLite):
# ------------------------------------------------------------------------------
class Role(db.Model):
    """Roles SQLAlchemy table."""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """Users SQLAlchemy table."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        """A write-only property. Attempting to read the password property
        will return an error"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """When the password property is set, the setter method will call Werkzeug’s
        generate_password_hash() function and write the result to the password_hash
        field."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check password with password hash, return True if matches."""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """Returns confirmation token."""
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'confirm': self.id}).decode('utf-8')

    def confirm_generated_token(self, token):
        """Try to deserialize the previously generated token, if the token expired,
        raise a SignalExpired exception, usually a message; 'The confirmation link is
        invalid or has expired'."""
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token.encode('utf-8'))
        except SignatureExpired:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token.encode('utf-8'))
        except SignatureExpired:
            return False
        user = User.query.get(data.get('reset'))
        if not user:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


# ------------------------------------------------------------------------------
# Flask-Login User Loading Function:
# ------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Return user object whenever flask-login loads a user from the database
    using user id, otherwise returns None."""
    return User.query.get(user_id)
