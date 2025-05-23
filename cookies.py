import os

from django.conf.global_settings import SECRET_KEY
from flask import session
from datetime import timedelta

from flask_session import Session

def init_app(app):
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server
    app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
    app.permanent_session_lifetime = timedelta(minutes=60)

def set_session(email, first_name, last_name):
    """Sets session data for the user."""
    session.permanent = True  # Makes the session permanent (so it persists across requests)
    session['email'] = email
    session['first_name'] = first_name
    session['last_name'] = last_name


def get_session():
    """Gets session data for the user."""
    email = session.get('email')
    user_data = {
        'email': email,
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name')
    }
    if not email:
        return None  # No valid session
    return user_data

def clear_session():
    """Clears session data for the user."""
    session.clear()
