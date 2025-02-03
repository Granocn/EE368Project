import string
import hashlib


def hashPass(password):
    data_to_hash = password
    hash_object = hashlib.sha256(data_to_hash.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest



def PasswordVerification(password):
    # Set all flags to 0
    l, u, p, d = 0, 0, 0, 0

    # check password length
    if (len(password) > 60):
        return "Invalid Password - Password too long!"

    elif (len(password) >= 8):

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
                return "Invalid Password : One or more characters are not allowed!"

        else:
            return ("Invalid Password : Please make sure your password has atleast one uppercase letter, "
                "one lowercase letter, one number, and one special character!")
    else:
        return "Invalid Password : Password too short!"

