from operator import truediv

from django.db.models import TextField
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
        elif request.form.get('signup') == "Sign up":
            return render_template('emailValidation.html')
        elif request.form.get('login') == "Log in":
            return render_template('userInfo.html')
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
