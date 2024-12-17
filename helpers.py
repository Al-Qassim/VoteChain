import requests
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from time import time, ctime

from cs50 import SQL
from functools import wraps


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

# Create tables
def create_tables_if_not_exist(db_path=""):
    if not os.path.exists(db_path):
        db = SQL("sqlite:///" + db_path)

        db.execute("""
            create table users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username text unique,
                hash_password text,
                phone_number text,
                signiture_private_key text,
                signiture_public_key text 
            );
        """)

        db.execute("""
            create table elections (
                election_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                discription text,
                deadline text,
                voting_system text,
                zkproof text,
                results text
            );
        """)

        db.execute("""
            create table candidates (
                candedate_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                election_id int,
                private_key text,
                public_key text 
            );
        """)

        db.execute("""
            create table votes (
                vote_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                election_id int,
                voting_ballot text,
            );
        """)


        # rolles Table
        #db.execute("""
        #    ceatre table rolles (
        #        roll_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        #        Permeations             TEXT,
        #        admin                   int,
        #        casher                  int
        #    )
        #""")

