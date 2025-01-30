"""
Here is a start to the Cookie / Session management for our project. Relatively simple, but have not been able to
fully test it with the rest of the project. As of right now, this does NOT refer to anything related to the
MySQL database.

To incorporate with the app.py in 'Master', simply add a 'set_session(username, email, 'FirstName', 'LastName')' after
a successful login.

Example:
    if user_data:
                checkUsername, checkPassword, email = user_data
                if username == checkUsername and password == checkPassword:
                    print("Login successful")
                    set_session(username, email, 'FirstName', 'LastName')        # Example of session setting
                    return render_template('userInfo.html', user=get_session())  # Display user info using session data
                else:
                    print("Login failed")

Feel free to make any edits necessary during the meet today (1/30). Let me know of any issues!
- Joe

"""

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
