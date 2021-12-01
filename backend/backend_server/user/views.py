from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
import re

# Create your views here.
def newUser(request, username, email, password):
    checked = password_check(password)
    if checked.get("password_ok"):
        user = User.objects.create_user(username, email, password)
        user.save()
    else:
        return JsonResponse(checked, safe = False)
    # user = User.objects.get(username = username)
    # if user is None:
        
    #     return True
    # else:
    #     return False
    
def changePassword(request, username, password, newpassword):
    user = User.objects.get(username = username)
    user = authenticate(username = username, password = password)
    if user is not None:
        checked = password_check(password)
        if checked.get("password_ok"):
            user.set_password(newpassword)
            user.save()
        else:
            return JsonResponse(checked, safe = False)

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }