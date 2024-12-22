import requests
import os

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from time import time, ctime
from datetime import datetime

from cs50 import SQL
from functools import wraps

import rsa

import pandas as pd

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def forget_password_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id_to_reset_password") is None:
            return redirect("/forgetPassword")
        return f(*args, **kwargs)

    return decorated_function

if __name__=="__main__":

    db = SQL("sqlite:///Database.db")
    pd.DataFrame(db.execute("select * from users")).to_csv("static/keys/test.csv")
