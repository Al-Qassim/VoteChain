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
# @login_required
def index():
    if request.method == "GET":
        polls = db.execute("""
            SELECT poll_id, users.user_id, title, username, deadline
            FROM polls 
            inner join users 
            on users.user_id = polls.user_id
        """)
        
        return render_template("homepage.html", polls = polls, login= session.get("user_id", 0))
    
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
            flash("Please provide username", "error")
            return render_template("login.html"), 400

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide password", "error")
            return render_template("login.html"), 403

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash_password"], request.form.get("username") + request.form.get("password")
        ):
            flash("invalid username and/or password", "error")
            return render_template("login.html"), 403

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
            flash("Please provide username", "error")
            return render_template("register.html"), 400
        
        elif not request.form.get("password"):
            flash("Please provide password", "error")
            return render_template("register.html"), 400
        
        elif not request.form.get("rewrite_password"):
            flash("Please rewrite password", "error")
            return render_template("register.html"), 400
        
        elif not request.form.get("phone_number"):
            flash("Please provide phone number", "error")
            return render_template("register.html"), 400
        
        # check user name not used username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            flash("Username already taken, choose another one", "error")
            return render_template("register.html"), 403

        # Ensure same password
        if request.form.get("password") != request.form.get("rewrite_password"):
            flash("Passwords don't match", "error")
            return render_template("register.html"), 403

        # record user name and hashed password

        db.execute(
            "insert into users (username, hash_password, phone_number, date) values (?, ?, ?, ?)",
            request.form.get("username"),
            generate_password_hash( request.form.get("username") + request.form.get("password") ),
            request.form.get("phone_number"),
            datetime.fromtimestamp(time()).strftime('%d-%m-%Y')
        )

        # Redirect user to login
        return redirect("/login")

@app.route('/forgetPassword', methods=["GET", "POST"])
def forgetPassword():
    if request.method == "GET":
        return render_template("forgetPassword.html",image_url='..\\images\\voteChain.jpg')
    elif request.method == "POST":
        if not request.form.get("username_or_phone_number"):
            flash("Please provide username or phone number", "error")
            return render_template("forgetPassword.html"), 400
        
        # check user name and phone number
        rows = db.execute("SELECT * FROM users WHERE username = ? or phone_number = ?", request.form.get("username_or_phone_number"), request.form.get("username_or_phone_number"))
        if len(rows) != 1:
            flash("no username or phone number match exist", "error")
            return render_template("forgetPassword.html"), 403
        
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
            flash("Please provide password", "error")
            return render_template("reset_password.html"), 400
        if not request.form.get("rewrite_password"):
            flash("Please rewrite password", "error")
            return render_template("reset_password.html"), 400
        
        # Ensure same password
        if request.form.get("password") != request.form.get("rewrite_password"):
            flash("Passwords don't match", "error")
            return render_template("reset_password.html"), 400

        # hashed change password 
        db.execute(
            "update users set hash_password = ?",
            generate_password_hash( session["username_to_reset_password"] + request.form.get("password") )
            )
                
        return redirect("/login")

@app.route("/voting_ballot")
@login_required
def voting_ballot():
    american_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqI97lBrpfjG7wo0zytKSKSStwS29FfYYL4Q&s'
    trump_pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1MWm4Uc-yhWB5bkRg8r_Vy6ueABFtDb_qSA&s'
    return render_template("voting-ballot.html",american_img=american_img, trump_pic=trump_pic, login= session.get("user_id", 0))

@app.route("/voter")
@login_required
def voter_page():
    american_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqI97lBrpfjG7wo0zytKSKSStwS29FfYYL4Q&s'
    trump_pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1MWm4Uc-yhWB5bkRg8r_Vy6ueABFtDb_qSA&s'
    kamala_pic = 'https://news.stanford.edu/__data/assets/image/0023/45950/Headshot_harris_vertical.jpeg'
    republican = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Republican_Disc.svg/1200px-Republican_Disc.svg.png'
    Vice_President = "JD Vance"
    republican_txt = "Republican"
    return render_template("listed_voter.html", american_img=american_img, trump_pic=trump_pic, Vice_President=Vice_President, kamala_pic=kamala_pic, republican=republican, republican_txt=republican_txt, login= session.get("user_id", 0))

@app.route("/create_poll", methods=["GET", "POST"])
@login_required
def creat_poll():
    if request.method == "GET":
        return render_template("create_poll.html", login= session.get("user_id", 0))
    
    elif request.method == "POST":
        # recive a erequest for creating poll, the request mast contain a title, candidates and the number of voters
        inputs = [
            "title",
            "date",
            "number_of_voters",
            #"discription",
            #"voting_system",
            "candidate_1",
            "candidate_2" # candidate_3, candidate_4, ...
        ]
        
        for i in inputs:
            if request.form.get(i, "") == "":
                flash(f"Please provide all fields, {i} is missing")
                return render_template("create_poll.html", login= session.get("user_id", 0)), 400
        number_of_candidates = 0
        for i in request.form:
            if i[:9] == "candidate":
                number_of_candidates += 1
        try:
            if int(request.form.get("number_of_voters")) < 1:
                raise Exception("Sorry, no numbers below one")
        except:
            flash("Please an integer for the number of voters")
            return render_template("create_poll.html", login= session.get("user_id", 0)), 400
        
        # check if the user have this title already
        if db.execute(
                "select * from polls where user_id = ? and title = ?;",
                session["user_id"],
                request.form.get("title")
            ):
            flash("title already used, please choose another one")
            return render_template("create_poll.html", login= session.get("user_id", 0)), 400
        # add new poll

        db.execute("""
            INSERT INTO polls (
                user_id,
                title,
                deadline,
                number_of_voters,
                discription,
                voting_system       
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                session["user_id"],
                request.form.get("title"),
                request.form.get("date"),
            int(request.form.get("number_of_voters")), # TODO: make sure the user give integer here 
                request.form.get("discription", ""),
                "Plurality"# request.form.get("voting_system")
        )

        # add candidates

        poll_id = db.execute("""
                select * from polls where user_id = ? and title = ?;
                """,
                session["user_id"],
                request.form.get("title")
            )[0]["poll_id"]
        
        for i in range(number_of_candidates):
            db.execute("""
            INSERT INTO candidates (
                candidate_name,
                poll_id,
                candidate_index
                ) VALUES (?, ?, ?)
            """,
                request.form.get(f"candidate_{i+1}"),
                poll_id,
                i+1
            )

        # save the poll image
        if request.files['Poll image']:
            file = request.files['Poll image']
            file.save("static/images/polls images/"+f"{poll_id}"+".png")
        
        # generate public and private keys
        for i in range(int(request.form.get("number_of_voters"))):
            ballot_encryption_key, ballot_decryption_key = rsa.newkeys(1024)
            db.execute("""
            INSERT INTO votes (
                poll_id,
                ballot_encryption_key,
                ballot_decryption_key
                ) VALUES (?, ?, ?)
            """,
                poll_id,
                ballot_encryption_key.save_pkcs1("PEM").decode(),
                ballot_decryption_key.save_pkcs1("PEM").decode()
            )

        return redirect("/account")

@app.route("/delete_poll", methods=["POST"])
@login_required
def delete():
    poll_id = int(request.form.get("poll_id")) # TODO security needed
    db.execute("""
        DELETE FROM polls WHERE poll_id = ?;
        """,
        poll_id
    ) 
    db.execute("""
        DELETE FROM candidates WHERE poll_id = ?;
        """,
        poll_id
    ) 
    db.execute("""
        DELETE FROM votes WHERE poll_id = ?;
        """,
        poll_id
    ) 
    if os.path.exists(f"static/images/polls images/{poll_id}.png"):
        os.remove(f"static/images/polls images/{poll_id}.png")
    return redirect("/account")

@app.route("/account", methods=["GET"])
@login_required
def account():
    if request.method == "GET":
        user_info = db.execute("SELECT user_id, username, phone_number, date FROM users WHERE user_id =? ",  session["user_id"])[0]
        polls = db.execute("SELECT * FROM polls WHERE user_id =? ",  session["user_id"])
        return render_template("account.html", user_info = user_info, polls = polls, login= session.get("user_id", 0))

@app.route("/admin_dashboard_poll", methods=["GET"])
@login_required
def admin_dashboard_poll():
    poll_id = int(request.args.get("poll_id"))
    poll = db.execute("SELECT * FROM polls WHERE poll_id = ? ", poll_id)[0]
    candidates =  db.execute("SELECT * FROM candidates WHERE poll_id = ? ", poll_id)
    counts = db.execute("select voting_ballot, count(*) as count from votes where poll_id = ? group by voting_ballot", poll_id)
    poll["Number_of_votes_so_far"] = 0
    # TODO return a summary of the results so far
    for i in range(len(candidates)):
        for j in range(len(counts)):
            candidates[i]["count"] = 0
            if f"{candidates[i]["candidate_index"]}"==counts[j].get("voting_ballot"):
                candidates[i]["count"] = counts[j].get("count")
                poll["Number_of_votes_so_far"] += counts[j]["count"]
                break
    for i in range(len(candidates)):
        candidates[i]["percentage"] = f"{candidates[i]["count"]/poll["Number_of_votes_so_far"]*100:0.1f}" if poll["Number_of_votes_so_far"] else 0
    return render_template("admin_dashboard_poll.html", poll = poll, candidates = candidates, login= session.get("user_id", 0))

@app.route("/poll", methods=["GET", "POST"])
def poll():
    if request.method == "GET":
        poll_id = int(request.args.get("poll_id"))
        poll = db.execute("SELECT * FROM polls WHERE poll_id = ? ", poll_id)[0]
        candidates =  db.execute("SELECT * FROM candidates WHERE poll_id = ? ", poll_id)
        # TODO return a summary of the results so far
        return render_template("poll.html", poll = poll, candidates = candidates, login= session.get("user_id", 0))
    
    elif request.method == "POST":
        inputs = [
            "encryptedMessage",
            "poll_id"
        ]
        r = request.get_json()
        try:
            int(r.get("poll_id"))
        except:
            print("poll_id is missing")
            flash("vote correctly and provide valid poll_id")
            return redirect("/")
        if not r.get("encryptedMessage"):
            print("encryptedMessage is missing")
            flash("please vote correctly and choose one of the candidates")
            return redirect("/poll?poll_id="+f"{r.get("poll_id")}")
        
        # make sure the voting key is correct, use the voting key and the poll_id
        # if not, flash a message
        # if yes, make sure the candidate_index is valid, i.e. 0 < candidate_index <= number of candidates
        # print("Your vote was sent successfully")
        # flash("Your vote was sent successfully")

        encrypted_message = r.get("encryptedMessage")
        encrypted_message_bytes = base64.b64decode(encrypted_message)
        ids_ballot_decryption_keys = [
            [a["vote_id"], rsa.PrivateKey.load_pkcs1(a["ballot_decryption_key"])] 
            for a in db.execute(
                "select vote_id, ballot_decryption_key from votes where poll_id = ?", r.get("poll_id")
            )
            ]
        number_of_candidates = int(db.execute(
                "select count(*) as count from candidates where poll_id = ?",
                r.get("poll_id")
            )[0]["count"])
        valid = 0
        for vote_id, ballot_decryption_key in ids_ballot_decryption_keys:
            try:
                decrypted_message = rsa.decrypt(encrypted_message_bytes, ballot_decryption_key).decode('utf-8')
                if (
                    int(decrypted_message) < 1 + number_of_candidates
                    and
                    int(decrypted_message) > 0
                    ):
                    valid = 1
                    break
            except:
                pass

        if not valid:
            print("votting ballot is not valid")
            flash("votting ballot is not valid")
            return {"message": "votting ballot is not valid"}, 400
        else:
            print("votting ballot is valid")
            flash("you have successfully voted")
        
        db.execute("update votes set voting_ballot =  ? where vote_id = ?", decrypted_message, vote_id)

        return {"message": "you have successfully voted"}, 200

@app.route("/about")
def about():
    return render_template("about_page.html",img1='..\\images\\voteChain.jpg', login= session.get("user_id", 0))

if __name__ == '__main__':
    app.run(debug=True)

