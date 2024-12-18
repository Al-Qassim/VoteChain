from helpers import *

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db_path = ""
db = SQL("sqlite:///Database.db")

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
    if request.method == "GET":
        return render_template("homepage.html",image_url='..\\images\\voteChain.jpg', image_url1='..\\images\\2024-us-election.png')
    elif request.method == "POST":
        pass

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in

    requist = {
        "username": value,
        "password": value
        }
    
    """

    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
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
            rows[0]["hash_password"], request.form.get("username") + request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user

    requist = {
        "username": value,
        "password": value,
        "rewrite_password": value,
        "phone_number": value
        }
    
    """
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        # Ensure all information was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("rewrite_password"):
            return apology("must rewrite password", 400)
        elif not request.form.get("phone_number"):
            return apology("must provide Phone Number", 400)
        
        # check user name not used username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            return apology("username already taken", 400)

        # Ensure same password
        if request.form.get("password") != request.form.get("rewrite_password"):
            return apology("not the same password", 400)

        # record user name and hashed password
        db.execute(
            "insert into users (username, hash_password, phone_number) values (?, ?, ?)",
            request.form.get("username"),
            generate_password_hash( request.form.get("username") + request.form.get("password") ),
            request.form.get("phone_number")
        )

        # Redirect user to login
        return redirect("/login")

@app.route('/forgetPassword', methods=["GET", "POST"])
def forgetPassword():
    if request.method == "GET":
        return render_template("forgetPassword.html")
    elif request.method == "POST":
        if not request.form.get("username_or_phone_number"):
            return apology("must provide username or phone number", 400)
        
        # check user name and phone number
        rows = db.execute("SELECT * FROM users WHERE username = ? or phone_number = ?", request.form.get("username_or_phone_number"), request.form.get("username_or_phone_number"))
        if len(rows) != 1:
            return apology("no username or phone number mach exist", 400)
        
        # Remember which user has logged in
        session["user_id_to_reset_password"] = rows[0]["user_id"]
        session["username_to_reset_password"] = rows[0]["username"]
        
        return redirect("/reset_password")

@app.route('/reset_password', methods=["GET", "POST"])
@forget_password_required
def resetPassword():
    if request.method == "GET":
        return render_template("reset_password.html")
    elif request.method == "POST":
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("rewrite_password"):
            return apology("must reset password", 400)
        
        # Ensure same password
        if request.form.get("password") != request.form.get("rewrite_password"):
            return apology("not the same password", 400)

        # hashed change password 
        db.execute(
            "update users set hash_password = ?",
            generate_password_hash( session["username_to_reset_password"] + request.form.get("password") )
            )
                
        return redirect("/login")

@app.route("/voting_ballot")
def voting_ballot():
    return render_template("voting-ballot.html")

@app.route("/voter")
def voter_page():
    american_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqI97lBrpfjG7wo0zytKSKSStwS29FfYYL4Q&s'
    trump_pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1MWm4Uc-yhWB5bkRg8r_Vy6ueABFtDb_qSA&s'
    kamala_pic = 'https://news.stanford.edu/__data/assets/image/0023/45950/Headshot_harris_vertical.jpeg'
    republican = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Republican_Disc.svg/1200px-Republican_Disc.svg.png'
    Vice_President = "JD Vance"
    republican_txt = "Republican"
    return render_template("listed_voter.html", american_img=american_img, trump_pic=trump_pic, Vice_President=Vice_President, kamala_pic=kamala_pic, republican=republican, republican_txt=republican_txt)


# recive a erequest for creating poll, the request mast contain a title, candidates and the number of voters
@app.route("/create_poll", methods=["GET", "POST"])
def creat_poll():
    if request.method == "GET":
        return render_template("create_poll.html")
    elif request.method == "POST":
        input = [
            "title",
            "number_of_voters",
            "candidates",
        ]
        return request.json


if __name__ == '__main__':
    app.run(debug=True)

