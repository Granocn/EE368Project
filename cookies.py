from flask import session
from datetime import timedelta

def init_app(app):
    """Initialize session configuration for the app."""
    app.secret_key = 'secret_key'  # We need a secret key for session management
    app.permanent_session_lifetime = timedelta(days=1)  # Sets the session lifetime duration (days or hours)

def set_session(username, email, first_name, last_name):
    """Sets session data for the user."""
    session.permanent = True  # Makes the session permanent (so it persists across requests)
    session['username'] = username
    session['email'] = email
    session['first_name'] = first_name
    session['last_name'] = last_name

def get_session():
    """Gets session data for the user."""
    user_data = {
        'username': session.get('username'),
        'email': session.get('email'),
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name')
    }
    return user_data

def clear_session():
    """Clears session data for the user."""
    session.clear()

def is_logged_in():
    """Checks if a user is logged in."""
    return 'username' in session
