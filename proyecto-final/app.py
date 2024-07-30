from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from login import login_required

# Initialize Flask app
app = Flask(__name__)

# Initialize sessions so as to use filesystems
app.config["SESSION PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure that responses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Initialize database
db = SQL("sqlite:///FL.db")

# My code
@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Get all of the variables needed
        username = request.form.get('username')
        email = request.form.get('email')
        password_1 = request.form.get('password-1')
        password_2 = request.form.get('password-2')

        # Check if any of the variables are mission
        if not email or not password_1 or not password_2:
            warning = "Missing passwords or email. Try again"
            return render_template("register.html", warning=warning)
        
        # Check if the passwords match
        if password_1 != password_2:
            warning = "Passwords don't match"
            return render_template("register.html", warning=warning)
        
        # Try to insert the username, email and passwords into the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password_1))
        except:
            # If something goes wrong, means that the username has been taken
            warning = "Username already in use. Try another one"
            return render_template("register.html", warning=warning)
        
        return redirect("/homepage")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Define variables
    username = request.form.get("username")
    password = request.form.get("password")En 

    # Check if the user typed these two
    if not username or not password:
        warning = "Username and/or password not typed"
        return render_template("login.html", warning=warning)
    
    # Take out rows from the database
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    # Check if the username exists and the password is correct
    if len(rows) != 1 or check_password_hash(rows[0]['password'], password):
        warning = "Invalid username and/or password. Try again"
        return render_template("login.html", warning=warning)
    
    # Remember which user has logged in
    session['user_id'] = rows[0]['id']
    
    # Redirect to the homepage
    return redirect("/homepage")