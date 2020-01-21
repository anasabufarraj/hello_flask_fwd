# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

import unittest
from flask import current_app
from application import create_app, db
from application.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User(password='secret')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='secret')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='secret')
        self.assertTrue(user.verify_password('secret'))
        self.assertFalse(user.verify_password('not secret'))

    def test_password_salts_are_random(self):
        user1 = User(password='secret')
        user2 = User(password='secret')
        self.assertTrue(user1.password_hash != user2.password_hash)
