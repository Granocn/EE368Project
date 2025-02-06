from operator import truediv

import mysql.connector
#from django.db.models import TextField
from flask import Flask, render_template, request, redirect, url_for, json

from passVer import *

from cookies import set_session, get_session

# from settings import Username, Password

app = Flask(__name__)

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
    global token
    global email

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
                cursor.execute(
                    "SELECT Email FROM Users WHERE Email = %s", (email,))

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
                        password = hashPass(password)

                        # Insert the info into the database
                        cursor.execute(
                            "INSERT INTO Users (FirstName, Email, Password, LastName) VALUES (%s, %s, %s, %s)",
                            (firstName, email, password, lastName))

                        token = MakeTokenSendEmail(email)

                        # Redirect the user
                        return render_template('emailVer.html')

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

                # set_session(email, 'FirstName', 'LastName')
                return render_template('userInfo.html', userVar = firstName + " " + lastName, userEmail = email)
                # return render_template('userInfo.html', user = get_session())
            else:
                print("Login failed")
                print(firstName)
                incorrect = "Incorrect email or password"
                return render_template('login.html', incorrect = incorrect)
            # return render_template('userInfo.html')
        elif request.form.get('forgotPass') == "Forgot Password":
            return render_template('forgotPassword.html')

        elif request.form.get('tokenSubmit') == "Submit":
            # Correct token is entered
            if request.form['token'] == token:
                # Commit the data
                mydb.commit()
                return render_template('login.html')
            # Incorrect token is entered
            else:
                token = MakeTokenSendEmail(email)
                return render_template('emailVer.html',
                                       incorrect = 'Error : Email Verification Failed\n'
                                                   'A new verification code has been sent!')

    return redirect(url_for('button'))


if __name__ == '__main__':
    app.run()
