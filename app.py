import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import mysql.connector
from passVer import *
from cookies import init_app, set_session, get_session

app = Flask(__name__)

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

#
# def loginclick():
#     if request.method == 'POST':
#         if request.form['login_button'] == 'Login':
#             # username = request.form['username']
#             # password = request.form['password']

@app.route('/', methods=["GET", "POST"])
def button():

    if request.method =="POST":
        if request.form.get('homePage') == "Home":
            return render_template("main.html")
        if request.form.get('userInfoPage') == "User Info":
            user_data = get_session()
            print(user_data)
            firstName = user_data['first_name']
            lastName = user_data['last_name']
            email = user_data['email']
            if (user_data['email'] == None):
                return render_template("main.html")
            else:
                return render_template("userInfo.html", userVar = firstName + " " + lastName, userEmail = email)
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

                set_session(email, firstName, lastName)
                user_data = get_session()
                print("Session data after login:", get_session())  # Debugging check
                return render_template('userInfo.html', userVar = firstName + " " + lastName, userEmail = email)

            else:
                print("Login failed")
                print(firstName)
                incorrect = "Incorrect email or password"
                return render_template('login.html', incorrect = incorrect)
            # return render_template('userInfo.html')
        elif request.form.get('forgotPass') == "Forgot Password":
            return render_template('forgotPassword.html')

    return redirect(url_for('button'))



if __name__ == '__main__':
    app.run()
