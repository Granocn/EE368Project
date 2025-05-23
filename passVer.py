import string
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sends an email to the specified recEmail
def SendEmail(email,body,sub):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("ee368project@gmail.com", "agbk izdf kpfe ssby")
    # Create a MIMEText object to represent the email
    msg = MIMEMultipart()
    msg['Subject'] = sub

    # Attach the body of the email to the message
    msg.attach(MIMEText(body, 'plain'))
    s.sendmail("ee368project@gmail.com", email, msg.as_string())
    # terminating the session
    s.quit()



# Purpose: Hash a password using SHA256
# Pre: The password being hashed
# Post: Returns the hashed password
def HashPass(password):
    data_to_hash = password
    hash_object = hashlib.sha256(data_to_hash.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest


# Purpose: Verifies the user's password meets the requirements
# Pre: The password being verified
# Post: Return an empty string if the password is good, returns
# an error message otherwise
def PasswordVerification(password):
    # Set all flags to 0
    l, u, p, d = 0, 0, 0, 0

    # Check the password minimum length
    if (len(password) >= 8):

        # iterate through each character
        for i in password:

            # counting lowercase alphabets
            if (i in string.ascii_lowercase):
                l += 1

            # counting uppercase alphabets
            elif (i in string.ascii_uppercase):
                u += 1

            # counting digits
            elif (i in string.digits):
                d += 1

            # counting the special characters
            elif (i in string.punctuation):
                p += 1

        # Check that all character requirements were met
        if (l >= 1 and u >= 1 and p >= 1 and d >= 1):

            # Check that no illegal characters were used
            if (l + p + u + d == len(password)):
                return ""
            else:
                return "Error : One or more characters are not allowed!"

        else:
            return ("Error : Please make sure your password has atleast one uppercase letter, "
                "one lowercase letter, one number, and one special character!")
    else:
        return "Error : Password too short, it must be at least 8 characters long!"



