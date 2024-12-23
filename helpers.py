import requests
import os

from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from time import time, ctime
from datetime import datetime

from cs50 import SQL
from functools import wraps

import rsa
import base64
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

def calculate_winner(poll_id, db):
    
    poll = db.execute("SELECT * FROM polls WHERE poll_id = ? ", poll_id)[0]

    if poll.get("results"):
        return poll.get("results"), poll.get("winner")

    candidates =  db.execute("SELECT * FROM candidates WHERE poll_id = ? ", poll_id)

    candidates =  db.execute("SELECT * FROM candidates WHERE poll_id = ? ", poll_id)
    counts = db.execute("select voting_ballot, count(*) as count from votes where poll_id = ? group by voting_ballot", poll_id)
    poll["Number_of_votes_so_far"] = 0

    for i in range(len(candidates)):
        for j in range(len(counts)):
            candidates[i]["count"] = 0
            if f"{candidates[i]["candidate_index"]}"==counts[j].get("voting_ballot"):
                candidates[i]["count"] = counts[j].get("count")
                poll["Number_of_votes_so_far"] += counts[j]["count"]
                break
    
    highest_count = max([a["count"] for a in candidates])
    winners = [a["candidate_name"] for a in candidates if a["count"] == highest_count]

    if len(winners) == 1:
        result = "win", winners[0]
    else: 
        result = "drow", " equals ".join(winners)
    
    db.execute("update polls set results = ?, winner = ? WHERE poll_id = ? ", result[0], result[1], poll_id)
    return result

if __name__=="__main__":
    db = SQL("sqlite:///Database.db")
    print(calculate_winner(41, db))

    # pd.DataFrame(db.execute("select * from users")).to_csv("static/keys/test.csv")
