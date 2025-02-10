import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from passVer import *
from cookies import *


app = Flask(__name__)

# Initialize session and secret key
init_app(app)
Session(app)

# Debugging check
#print("Current SECRET_KEY:", app.secret_key)  # Ensure it's not None


mydb = mysql.connector.connect(
    host="54.172.50.181",
    user="admin",
    password="Pawc10mk1???",
    database="ee368project"
)


cursor = mydb.cursor()

@app.route('/')
def main():
    user_data = get_session()
    firstName = user_data['first_name']
    lastName = user_data['last_name']
    email = user_data['email']
    if (user_data['email'] == None):
        return render_template("main.html")
    else:
        return render_template("userInfo.html", userVar=firstName + " " + lastName, userEmail=email)


@app.route('/', methods=["GET", "POST"])
def button():
    global token        # Access token for various verifications
    global email        # User email
    global firstName    # User first name
    global lastName     # User last name
    global password     # User password
    global forgotFlag

    if request.method =="POST":

        if request.form.get('loginPage') == "Log in":
            return render_template("login.html")

        elif request.form.get('signupPage') == "Sign up":
            return render_template("signup.html")

        elif request.form.get('homePage') == "Home":
            # user_data = get_session()
            # firstName = user_data['first_name']
            # lastName = user_data['last_name']
            # email = user_data['email']
            # if (user_data['email'] == None):
            #     return render_template("main.html")
            # else:
            #     return render_template("userInfo.html", userVar=firstName + " " + lastName, userEmail=email)
            return render_template("main.html")

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
                            emailMess = ("To complete your registration for your EE368Project account please use the following verification code.\n\n"
                                         "Verification Code: ") + token + ("\n\n\nIf you are not trying to register this email address, "
                                                                                 "please ignore this.")
                            # Send the email
                            SendEmail(email,emailMess,"Email Verification - ["+token+"]")

                            # Set the forgot flag to false - lets the application know what the tokens purpose is
                            # ie. for account verification or password resetting
                            forgotFlag = False

                            # Redirect the user
                            return render_template('emailVer.html',
                                                   header = 'A verification code has been sent to '+ email)
                        except:
                            # Display the error to the user
                            return render_template('signup.html',
                                                   incorrect='Error : Email Address Cannot be Found!')

                    # Password did not pass
                    else:
                        # Display the error to the user
                        return render_template('signup.html', incorrect = passMess)

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

            cursor.execute("SELECT FirstName, Password, Email, LastName FROM Users WHERE Email = %s AND Password = %s", (email, password))

            for (FirstName, Password, Email, LastName) in cursor:
                firstName = FirstName
                checkEmail = Email
                checkPassword = Password
                lastName = LastName

            # Successful login
            if( email == checkEmail and password == checkPassword):

                # Begin new session
                set_session(email, firstName, lastName)
                #print("Session data after login:", get_session())  # Debugging check

                return render_template('userInfo.html',
                                       userVar = firstName + " " + lastName, userEmail = email)


            # Login Unsuccessful
            else:
                return render_template('login.html', incorrect = "Error : Incorrect email or password")

        elif request.form.get('forgotPass') == "Forgot Password":
            return render_template('forgotPassword.html')

        elif request.form.get('tokenSubmit') == "Submit":

            if forgotFlag:
                # Correct token is entered
                if request.form['token'] == token:
                    return render_template('resetPassword.html')
                else:
                    return render_template('forgotPassword.html',
                                           incorrect = "Error : Invalid code please try again!")

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
                    emailMess = ("To complete your registration for your EE368Project account please use the following verification code.\n\n"
                                 "Verification Code: ") + token + ("\n\n\nIf you are not trying to register this email address, "
                                 "please ignore this.")
                    # Send the email
                    SendEmail(email, emailMess, "Email Verification - ["+token+"]")

                    return render_template('emailVer.html',
                                           header = 'A new verification code has been sent to '+ email,
                                           incorrect = 'Error : Email Verification Failed!')

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
                                 "Verification Code: ") + token + ("\n\n\nIf you are not trying to reset your password, "
                                 "please ignore this email.")
                    # Send the email
                    SendEmail(email, emailMess, "Forgotten Password - ["+token+"]")

                    # Set the forgot flag to false - lets the application know what the tokens purpose is
                    # ie. for account verification or password resetting
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
                    cursor.execute("UPDATE Users SET Password = %s WHERE Email = %s;", (password,email))

                    # Commit the data
                    mydb.commit()

                    # Clear the cookie session to be safe
                    clear_session()

                    # Return them to login
                    return render_template('login.html')

                else:
                    return render_template('resetPassword.html',
                                           incorrect = passMess)

            else:
                return render_template('resetPassword.html',
                                       incorrect = "Error : Passwords must match!")

    return redirect(url_for('button'))


if __name__ == '__main__':
    app.run()
