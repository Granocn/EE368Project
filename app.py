from operator import truediv

import mysql.connector
#from django.db.models import TextField
from flask import Flask, render_template, request, redirect, url_for

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

mydb = mysql.connector.connect(
  host="128.153.174.210",
  user="EE368Project",
  password="password123",
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
            username = request.form['username']
            secureQuestion = request.form['secureAnswer']
            if request.form['email'] == request.form['email2']:
                email = request.form['email']
            else:
                print("Emails don't match")
                email = "NULL"
            #             # email = request.fm['email']
            if request.form['password'] == request.form['password2']:
                password = request.form['password']
            else:
                print("Passwords don't match")
                password = "NULL"
            print(username, email, password, secureQuestion)
            cursor.execute("INSERT INTO Users (Username, Email, Password, SecureQuestion) VALUES (%s, %s, %s, %s)", (username, email, password, secureQuestion))
            # cursor.close()
            mydb.commit()
            # return username, email, password
            return render_template('login.html')
        elif request.form.get('login') == "Log in":
            incorrect = ""
            password = request.form['password']
            email = request.form['email']
            checkEmail = ""
            checkPassword = ""
            cursor.execute("SELECT Username, Password, Email FROM Users WHERE Email = %s AND Password = %s", (email, password))
            for (Username, Password, Email) in cursor:
                username = Username
                checkEmail = Email
                checkPassword = Password
            if( email == checkEmail and password == checkPassword):
                print("Login successful")

                return render_template('userInfo.html', userVar = username, userEmail = email)
            else:
                print("Login failed")
                incorrect = "Incorrect email or password"
                return render_template('login.html', incorrect = incorrect)
            # return render_template('userInfo.html')
        elif request.form.get('forgotPass') == "Forgot Password":
            return render_template('forgotPassword.html')
    return redirect(url_for('button'))


# def passcheck():
#     # if render_template.__name__ == 'signup.html':
#         if request.method == 'POST':
#             if request.form.get('signup') == "Sign up":
#                 if request.form.get('password') == request.form.get('password2'):
#                     return render_template('main.html')
#                 else: return render_template('signup.html')
#             if request.form.get('login') == "Log in":
#                 return render_template('signup.html')
#             # else:
#             #     return render_template('login.html')


if __name__ == '__main__':
    app.run()
