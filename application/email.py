# ------------------------------------------------------------------------------
#  Copyright (c) 2020. Anas Abu Farraj.
# ------------------------------------------------------------------------------

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from application import mail


# ------------------------------------------------------------------------------
# Asynchronous Email Sending Setup:
# ------------------------------------------------------------------------------
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, template_name, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=app.config['APP_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['APP_MAIL_SENDER'],
                  recipients=[recipients])
    # TODO: Remove the assertion when finish testing
    assert msg.sender == 'Admin <goyoomed@gmail.com>'
    msg.body = render_template(template_name + '.txt', **kwargs)
    msg.html = render_template(template_name + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
