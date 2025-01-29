from pathlib import Path
import mysql.connector
from flask import Flask, render_template

# app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="EE368Project",
  password="password123",
  database="ee368project"
)

cursor = mydb.cursor()
# query = "SELECT Username, Password, Email FROM Users"
# cursor.execute(query)
# cursor.execute("SELECT * FROM Users")
#
username = "Cng1228"
password = "password123"
cursor.execute("SELECT Username, Password FROM Users WHERE Username = %s AND Password = %s", (username, password))
# def queryData():
# for (Username, Password, Email, SecureQuestion) in cursor:
#   print("{}, {}, {}, {}".format(Username, Password, Email, SecureQuestion))
# testRow = cursor.fetchone()
# print(testRow)
#
for (Username, Password) in cursor:
  print("{}, {}".format(Username, Password))


# *database example*

# DATABASES = {
#     'ee368project': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'university',
#         'USER': 'USER',
#         'HOST': '127.0.0.1',
#         'PORT': 3306,
#         'PASSWORD': 'Ajnh3nry'
#     }
# }
