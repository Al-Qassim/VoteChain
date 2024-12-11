import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from time import time, ctime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # TODO
    if request.method == "POST":
        deposite = request.form.get("deposite")
        if not deposite:
            return apology("please enter a deposite")
        try:
            deposite = float(deposite)
        except:
            return apology("please enter a number for the deposite")

        cash = db.execute(
            "select cash from users where id = ?",
            session["user_id"]
        )[0]["cash"]

        db.execute(
            "update users set cash = ? where id = ?;",
            cash + deposite, session["user_id"]
        )

        return redirect("/")
    else:
        data = db.execute(
                "SELECT symbol, sum(shares*BuyOrSell) as shares FROM transactions WHERE user_id = ? group by symbol;",
                session["user_id"]
            )
        data = [r for r in data if r["shares"] != 0]

        grandTotal = 0
        for r in data:
            q = lookup(r["symbol"])
            r["currentPrice"] = q["price"]
            r["value"] = r["currentPrice"]*r["shares"]
            r["stock"] = q["name"]
            grandTotal += r["value"]

        cash = db.execute(
            "select cash from users where id = ?",
            session["user_id"]
        )[0]["cash"]
        grandTotal += cash
        return render_template("index.html", data=data, cash=cash, grandTotal=grandTotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # TODO
    if request.method == "POST":
        # get the user inputs
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("please enter a symbol")

        shares = request.form.get("shares")
        if not shares:
            return apology("please enter a valid number for shares")
        try:
            shares = int(shares)
        except:
            return apology("please enter a valid number for shares")
        if shares <= 0:
            return apology("please enter a valid posative number for shares")
        # get the stock price and calculate the total cost
        q = lookup(symbol)
        if not q:
            return apology("no such symbol exist, please ented a valid symbol")

        TotalCost = q["price"]*shares
        UserBalance = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]

        if TotalCost > UserBalance:
            return apology(f"You Don't have enough cash\nyour order cost {TotalCost}\nyour balance is {UserBalance}")

        # record the transaction
        db.execute(
            "insert into transactions (user_id, BuyOrSell, shares, symbol, price, time) values (?, ?, ?, ?, ?, ?);",
            session["user_id"], 1, shares, symbol, q["price"], time()
        )
        db.execute(
            "update users set cash = ? where id = ?;",
            UserBalance - TotalCost, session["user_id"]
        )

        return redirect("/")

    else:
        print("")
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # TODO
    data = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?;",
            session["user_id"]
        )

    for r in data:
        r["value"] = r["price"]*r["shares"]
        r["time"] = ctime(float(r["time"]))
        r["BuyOrSell"] = "Buy" if r["BuyOrSell"] == 1 else "Sell"

    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # TODO
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("please enter a symbol")
        q = lookup(symbol)
        if not q:
            return apology("no such symbol exist, please ented a valid symbol")

        return render_template("quoted.html", q=q)
    else:
        #lookup("NFLX")
        # {'name': 'Netflix Inc. Common Stock', 'price': 667.82, 'symbol': 'NFLX'}

        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # TODO
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username doesn't exist
        if len(rows) != 0:
            return apology("username already taken", 400)

        # Ensure same password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("not the same password", 400)

        # record user name and hashed password
        db.execute(
            "insert into users (username, hash) values (?, ?)",
            request.form.get("username"),
            generate_password_hash( request.form.get("password") )
        )

        # Redirect user to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # TODO
    if request.method == "POST":
        # get the user inputs
        # get the user inputs
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("please enter a symbol")

        shares = request.form.get("shares")
        if not shares:
            return apology("please enter a valid number for shares")
        try:
            shares = int(shares)
        except:
            return apology("please enter a valid number for shares")
        if shares <= 0:
            return apology("please enter a valid posative number for shares")

        # get the databace
        try:
            data = db.execute(
                "SELECT symbol, sum(shares*BuyOrSell) as shares FROM transactions WHERE user_id = ? and symbol = ?;",
                session["user_id"], symbol
            )
        except:
            return apology("please choose a stock that you own")

        if shares > data[0]["shares"]:
            return apology("you don't have that many shares!")

        cash = db.execute(
            "select cash from users where id = ?",
            session["user_id"]
        )[0]["cash"]

        # get the price
        q = lookup(data[0]["symbol"])

        # record transaction
        db.execute(
            "insert into transactions (user_id, BuyOrSell, shares, symbol, price, time) values (?, ?, ?, ?, ?, ?);",
            session["user_id"], -1, shares, symbol, q["price"], time()
        )
        # update cash
        db.execute(
            "update users set cash = ? where id = ?;",
            cash + q["price"] * shares, session["user_id"]
        )

        return redirect("/")
    else:
        symbols = [
            r["symbol"]
            for r in db.execute(
                "SELECT symbol, sum(shares*BuyOrSell) as shares FROM transactions WHERE user_id = ? group by symbol;",
                session["user_id"]
                )
            if r["shares"] != 0
            ]
        return render_template("sell.html", symbols = symbols)
