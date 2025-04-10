import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from passVer import *
from cookies import *
import random
from authlib.integrations.flask_client import OAuth  # pip install flask requests authlib

app = Flask(__name__)
app.secret_key = "666666"

# Initialize session and secret key
init_app(app)
Session(app)

# Debugging check
# print("Current SECRET_KEY:", app.secret_key)  # Ensure it's not None

mydb = mysql.connector.connect(
    host="54.172.50.181",
    user="admin",
    password="Pawc10mk1???",
    database="ee368project"
)

cursor = mydb.cursor()

######################################################################

# OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='589973263454-m0qhjjp5qkom24okc1s3ghfghuu8uefg.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
)


@app.route('/auth/google')
def authGoogle():
    return google.authorize_redirect(url_for('authorizeGoogle', _external=True))


@app.route('/authGoogle/callback')
def authorizeGoogle():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    # Map the keys to what get_session() expects
    session['first_name'] = user_info.get('given_name')
    session['last_name'] = user_info.get('family_name')
    session['email'] = user_info.get('email')

    # Optionally, can also store the whole user_info if needed
    session['user'] = user_info
    return redirect('/userInfo')


# Github OAuth
github = oauth.register(
    name='github',
    client_id='Ov23likj13chtyyolFYf',
    client_secret='66d88938f145c9344ab90601269db1a09baf98a1',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'read:user user:email'},

)


@app.route('/auth/github')
def authGithub():
    return github.authorize_redirect(url_for('authorizeGit', _external=True))


@app.route('/authgithub/callback')
def authorizeGit():
    try:
        token = github.authorize_access_token()
        resp = github.get('user')
        user_info = resp.json()

        # store user's email if available
        email_resp = github.get('user/emails')
        emails = email_resp.json()  # list emails associated with GitHub account
        email = None
        for e in emails:
            if e['primary']:
                email = e['email']
                break
        print(f"Email: {email}")  # log the email

        # Store relevant user info in the session
        session['first_name'] = user_info.get('login')
        session['last_name'] = user_info.get('name', 'No name available')
        session['email'] = email

        return redirect('/userInfo')

    except Exception as e:
        print(f"Error during GitHub authorization callback: {e}")  # Debugging
        return f"Error during GitHub authorization callback: {e}", 500


custom_oauth_server = oauth.register(
    name='custom',
    client_id='client_123',
    client_secret='VIOFTZSdlVr8wZlWnR3sMYKk6Ib1qAdoRfv4WNviwOZun1Ir',
    access_token_url='http://127.0.0.1:5001/oauth/token',
    authorize_url='http://127.0.0.1:5001/oauth/authorize',
    api_base_url='http://127.0.0.1:5001/oauth/',
    client_kwargs={'scope': 'profile'},
)


@app.route('/login/callback')
def authorizeCustom():
    token = custom_oauth_server.authorize_access_token()  # ERROR
    resp = custom_oauth_server.get('userinfo')
    user_info = resp.json()
    # Map the keys to what get_session() expects
    session['first_name'] = user_info.get('name')
    session['email'] = user_info.get('email')
    return redirect('/userInfo')


@app.route('/login')
def loginCustom():
    return custom_oauth_server.authorize_redirect(url_for('authorizeCustom', _external=True))


########################################################################

@app.route('/')
def main():
    user_data = get_session()
    firstName = user_data.get('first_name')
    lastName = user_data.get('last_name')
    email = user_data.get('email')
    if email is None:
        return render_template("main.html")
    elif lastName is None:
        return render_template("userInfo.html", userVar=firstName, userEmail=email)
    else:
        return render_template("userInfo.html", userVar=firstName + " " + lastName, userEmail=email)


@app.route('/userInfo')
def user_info():
    user_data = get_session()
    if not user_data:
        print("No user data in session")
        return redirect(url_for('main'))
    firstName = user_data.get('first_name')
    lastName = user_data.get('last_name')
    email = user_data.get('email')
    bio = user_data.get('bio')
    if email is None:
        print("Email is none")
        return redirect(url_for('main'))

    # assign default values for users without first or last name
    if firstName is None and lastName is None:
        full_name = "User"
    elif lastName is None:
        full_name = firstName
    else:
        full_name = f"{firstName} {lastName}"

    return render_template("userInfo.html",
                           userVar=full_name,
                           userEmail=email,
                           userBio=bio)


@app.route('/postMain')
def post_main():
    user_data = get_session()
    firstName = user_data.get('first_name')
    lastName = user_data.get('last_name')
    email = user_data.get('email')
    if email is None:
        return redirect(url_for('main'))

    # Ensure neither firstName nor lastName is None
    if firstName is None:
        return render_template("postMain.html", userVar="User")
    elif lastName is None:
        return render_template("postMain.html", userVar=firstName)

    return render_template("postMain.html", userVar=firstName + " " + lastName)


@app.route('/logout')
def logout():
    clear_session()
    session.pop('user', None)
    return redirect('/')


@app.route('/', methods=["GET", "POST"])
def button():
    global token  # Access token for various verifications
    global email  # User email
    global firstName  # User first name
    global lastName  # User last name
    global password  # User password
    global forgotFlag

    if request.method == "POST":

        if request.form.get('loginPage') == "Log in":
            return render_template("login.html")

        elif request.form.get('signupPage') == "Sign up":
            return render_template("signup.html")

        elif request.form.get('homePage') == "Home":
            # For logged in users, redirect to postMain page
            return render_template("postMain.html", userVar=firstName + " " + lastName)

        elif request.form.get('signup') == "Sign up":
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']

            # Check for empty first and last names
            if firstName == "" or lastName == "":
                # Display the error to the user
                return render_template('signup.html',
                                       incorrect='Error : Both a first and last name must be entered!')

            # Check for empty email
            elif email == "":
                # Display the error to the user
                return render_template('signup.html',
                                       incorrect='Error : An email must be entered!')

            # Check that the emails match
            elif email == request.form['email2']:
                # Search for the email in the database
                cursor.execute("SELECT Email FROM Users WHERE Email = %s", (email,))

                # If the email is found its type will be tuple, not none
                if cursor.fetchone() is not None:
                    # Display the error to the user
                    return render_template('signup.html',
                                           incorrect='Error : An account with this email already exists!')

                # Check that the passwords match
                elif request.form['password'] == request.form['password2']:
                    password = request.form['password']

                    # Determine if the password passes verification
                    passMess = PasswordVerification(password)

                    # Check for passing
                    if passMess == "":
                        # Hash the password
                        password = HashPass(password)
                        try:
                            # Get a random token
                            token = str(random.randint(100000, 999999))

                            # Make the email message
                            emailMess = (
                                            "To complete your registration for your EE368Project account please use the following verification code.\n\n"
                                            "Verification Code: ") + token + (
                                            "\n\n\nIf you are not trying to register this email address, please ignore this.")

                            # Send the email
                            SendEmail(email, emailMess, "Email Verification - [" + token + "]")

                            # Set the forgot flag to false - lets the application know what the token's purpose is
                            forgotFlag = False

                            # Redirect the user
                            return render_template('emailVer.html',
                                                   header='A verification code has been sent to ' + email)
                        except:
                            # Display the error to the user
                            return render_template('signup.html',
                                                   incorrect='Error : Email Address Cannot be Found!')
                    # Password did not pass
                    else:
                        # Display the error to the user
                        return render_template('signup.html', incorrect=passMess)

                # Passwords did not match
                else:
                    # Display the error to the user
                    return render_template('signup.html',
                                           incorrect='Error : Passwords must match!')
            # Emails did not match
            else:
                # Display the error to the user
                return render_template('signup.html',
                                       incorrect='Error : Emails must match!')

        elif request.form.get('login') == "Log in":
            # Hash the password they input
            password = HashPass(request.form['password'])
            email = request.form['email']
            checkEmail = ""
            checkPassword = ""
            cursor.execute("SELECT FirstName, Password, Email, LastName FROM Users WHERE Email = %s AND Password = %s",
                           (email, password))
            for (FirstName, Password, Email, LastName) in cursor:
                firstName = FirstName
                checkEmail = Email
                checkPassword = Password
                lastName = LastName

            # Successful login
            if email == checkEmail and password == checkPassword:
                # Begin new session
                set_session(email, firstName, lastName)

                # print("Session data after login:", get_session())  # Debugging check
                return render_template('userInfo.html',
                                       userVar=firstName + " " + lastName, userEmail=email)
            # Login Unsuccessful
            else:
                return render_template('login.html', incorrect="Error : Incorrect email or password")

        elif request.form.get('forgotPass') == "Forgot Password":
            return render_template('forgotPassword.html')

        elif request.form.get('tokenSubmit') == "Submit":
            # Correct token is entered
            if forgotFlag:
                if request.form['token'] == token:
                    return render_template('resetPassword.html')
                else:
                    return render_template('forgotPassword.html',
                                           incorrect="Error : Invalid code please try again!")
            else:
                # Correct token is entered
                if request.form['token'] == token:
                    # Insert the info into the database
                    cursor.execute("INSERT INTO Users (FirstName, Email, Password, LastName) VALUES (%s, %s, %s, %s)",
                                   (firstName, email, password, lastName))
                    # Commit the data
                    mydb.commit()
                    return render_template('login.html')
                # Incorrect token is entered
                else:
                    # Get a random token
                    token = str(random.randint(100000, 999999))
                    # Make the email message
                    emailMess = (
                                    "To complete your registration for your EE368Project account please use the following verification code.\n\n"
                                    "Verification Code: ") + token + (
                                    "\n\n\nIf you are not trying to register this email address, please ignore this.")
                    # Send the email
                    SendEmail(email, emailMess, "Email Verification - [" + token + "]")
                    return render_template('emailVer.html',
                                           header='A new verification code has been sent to ' + email,
                                           incorrect='Error : Email Verification Failed!')

        elif request.form.get('forgotPassEmail') == "Submit":
            # Get the email the user provided
            email = request.form['email']

            # Search for the email in the database
            cursor.execute("SELECT Email FROM Users WHERE Email = %s", (email,))
            # If the email is found its type will be tuple, not none
            if cursor.fetchone() is None:
                # Display the error to the user
                return render_template('forgotPassword.html',
                                       incorrect='Error : No account found using this email!')
            else:
                try:
                    # Get a random token
                    token = str(random.randint(100000, 999999))
                    # Make the email message
                    emailMess = ("We've received a request to reset your password for your EE368Project account.\n\n"
                                 "Please use the following one-time verification code to reset your password.\n\n"
                                 "Verification Code: ") + token + (
                                    "\n\n\nIf you are not trying to reset your password, please ignore this email.")
                    # Send the email
                    SendEmail(email, emailMess, "Forgotten Password - [" + token + "]")
                    # Set the forgot flag to true - lets the application know what the token's purpose is
                    forgotFlag = True
                    return render_template('emailVer.html',
                                           header='A recovery code has been sent to ' + email)
                except:
                    return render_template('forgotPassword.html',
                                           incorrect='Error : Email Unreachable!')

        elif request.form.get('passReset') == "Submit":
            # Check that the passwords match
            if request.form['password'] == request.form['password2']:
                password = request.form['password']
                # Determine if the password passes verification
                passMess = PasswordVerification(password)
                # Check for passing
                if passMess == "":
                    # Hash the password
                    password = HashPass(password)
                    # Change the password in the database
                    cursor.execute("UPDATE Users SET Password = %s WHERE Email = %s;", (password, email))
                    # Commit the data
                    mydb.commit()
                    # Clear the cookie session to be safe
                    clear_session()
                    # Return them to login
                    return render_template('login.html')
                else:
                    return render_template('resetPassword.html',
                                           incorrect=passMess)
            else:
                return render_template('resetPassword.html',
                                       incorrect="Error : Passwords must match!")
    return redirect(url_for('button'))


if __name__ == '__main__':
    app.run()
