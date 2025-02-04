from operator import truediv

import mysql.connector
#from django.db.models import TextField
from flask import Flask, render_template, request, redirect, url_for

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
    return redirect(url_for('button'))


if __name__ == '__main__':
    app.run()
