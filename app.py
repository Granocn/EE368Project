import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app, render_template_string
from flask_session import Session
import mysql.connector
from passVer import *
from cookies import init_app, set_session, get_session
from forms import *
from itsdangerous import URLSafeTimedSerializer
from resetEmailContent import reset_password_email_html_content
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECURITY_PASSWORD_SALT'] = 'your_salt_value_here'

# Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail as SMTP server
app.config['MAIL_PORT'] = 587  # TLS port
app.config['MAIL_USE_TLS'] = True  # use tls
app.config['MAIL_USE_SSL'] = False  # avoid ssl
app.config['MAIL_USERNAME'] = 'oauthproject397@gmail.com'  # project email
app.config['MAIL_PASSWORD'] = 'qumr lgry ejrg nrtp'  # generated app password
app.config['MAIL_DEFAULT_SENDER'] = 'oauthproject397@gmail.com'

# Initialize flask mail
mail = Mail(app)

# Initialize session and secret key
init_app(app)
Session(app)

# Debugging check
print("Current SECRET_KEY:", app.secret_key)  # Ensure it's not None

#
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="EE368Project",
#   password="password123",
#   database="ee368project"
# )
# mysql.connector.

# mydb = mysql.connector.connect(
#   host="128.153.174.210",
#   user="EE368Project",
#   password="password123",
#   database="ee368project"
# )

mydb = mysql.connector.connect(
    host="54.172.50.181",
    user="admin",
    password="Pawc10mk1???",
    database="ee368project"
)


cursor = mydb.cursor()
# query = "SELECT Username, Password, Email FROM Users"
# cursor.execute(query)
# cursor.execute("SELECT * FROM Users")


@app.route('/')
def main():  # put application's code here
    return render_template('main.html')


# def loginclick():
#     if request.method == 'POST':
#         if request.form['login_button'] == 'Login':
#             # username = request.form['username']
#             # password = request.form['password']

@app.route('/', methods=["GET", "POST"])
def button():
    if request.method =="POST":
        if request.form.get('loginPage') == "Log in":
            return render_template("login.html")
        elif request.form.get('signupPage') == "Sign up":
            return render_template("signup.html")
        elif request.form.get('homePage') == "Home":
            return render_template("main.html")
        elif request.form.get('signup') == "Sign up":
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            if request.form['email'] == request.form['email2']:
                email = request.form['email']
            else:
                print("Emails don't match")
                email = "NULL"
            #             # email = request.fm['email']
            if request.form['password'] == request.form['password2']:
                password = request.form['password']

                # Determine if the password passes verification
                passMess = PasswordVerification(password)

                # Check for passing
                if passMess == "":
                    password = hashPass(password)
                # Password did not pass
                else:
                    print(passMess)  # Display this to the user
                    password = "NULL"
            else:
                print("Passwords don't match")
                password = "NULL"
            print(firstName, email, password, lastName)
            cursor.execute("INSERT INTO Users (FirstName, Email, Password, LastName) VALUES (%s, %s, %s, %s)", (firstName, email, password, lastName))
            # cursor.close()
            mydb.commit()
            # return username, email, password
            return render_template('login.html')
        elif request.form.get('login') == "Log in":
            # incorrect = ""
            password = hashPass(request.form['password'])
            print(password)
            email = request.form['email']
            checkEmail = ""
            checkPassword = ""
            firstName = ""
            cursor.execute("SELECT FirstName, Password, Email, LastName FROM Users WHERE Email = %s AND Password = %s", (email, password))
            for (FirstName, Password, Email, LastName) in cursor:
                firstName = FirstName
                checkEmail = Email
                checkPassword = Password
                lastName = LastName
            if( email == checkEmail and password == checkPassword):
                print("Login successful")

                set_session(firstName, email, firstName, lastName)
                print("Session data after login:", get_session())  # Debugging check
                return render_template('userInfo.html', userVar = firstName + " " + lastName, userEmail = email)
                user_data = get_session()
            else:
                print("Login failed")
                print(firstName)
                incorrect = "Incorrect email or password"
                return render_template('login.html', incorrect = incorrect)
            # return render_template('userInfo.html')
        elif request.form.get('forgotPass') == "Forgot Password":
            return redirect(url_for('forgot_password'))
    return redirect(url_for('button'))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        # Query for user by email
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user_data = cursor.fetchall()  # Fetch all matching users

        if user_data:
            user = user_data[0]  # Take the first user, if there is more than one

            try:
                user_email = user[2]  # Email = index 2
                send_mail(user_email)  # Send the email using user email
                flash('Your request has been sent. Check your email.', 'success')
            except IndexError as e:
                print(f"Error accessing user fields: {e}") #Debugging
                flash('An error occurred while processing your request.', 'danger')
        else:
            print("Invalid email or password")  # Debugging
            flash('No registered user', 'danger')

    return render_template('forgotPassword.html', title='Forgot Password', form=form)

#Generate a reset password token using email
def generate_reset_password_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


# Validate the reset token
def validate_reset_password_token(token):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=3600)  # Token valid for 1 hour
        return email
    except Exception as e:
        return None  # Token is invalid or expired


#Send flask mail
def send_mail(user_email):
    reset_password_url = url_for(
        "reset_password",
        token=generate_reset_password_token(user_email),
        _external=True,
    )

    # access resetEmailContent
    email_body = render_template_string(reset_password_email_html_content, reset_password_url=reset_password_url)

    # Create the message
    message = Message(
        subject="Reset your password",
        body=email_body,
        recipients=[user_email],
    )
    message.html = email_body

    if mail is not None:
        try:
            mail.send(message)
            print("Email sent successfully.") # Debugging
        except Exception as e:
            current_app.logger.error(f"Error sending email with Flask-Mail: {e}")
            print(f"Error sending email: {e}")  # Debugging


# Reset password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # ensure token is valid
    try:
        email = validate_reset_password_token(token)
    except:
        flash('The token is invalid or expired', 'danger')
        return redirect(url_for('forgot_password'))

    # If token is valid, proceed to reset password form
    form = newPasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        # Save new password to database
        cursor.execute("UPDATE Users SET Password = %s WHERE Email = %s", (new_password, email))
        mydb.commit()

        flash('Your password has been reset:)', 'success')
        return render_template("login.html") #return user to login view

    return render_template('resetPassword.html', form=form)

if __name__ == '__main__':
    app.run()
