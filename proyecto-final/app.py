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
db = SQL("sqlite:///fl.db")

# My code
@app.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Get all of the variables needed
        username = request.form.get('username')
        name = request.form.get('name')
        last_name = request.form.get('last-name')
        password_1 = request.form.get('password-1')
        password_2 = request.form.get('password-2')

        # Check if any of the variables are mission
        if not username or not password_1 or not password_2 or not name or not last_name:
            warning = "Missing passwords, full name and/or email. Try again"
            return render_template("register.html", warning=warning)
        
        # Check if the passwords match
        if password_1 != password_2:
            warning = "Passwords don't match"
            return render_template("register.html", warning=warning)
        
        # Try to insert the username, email and passwords into the database
        try:
            db.execute("INSERT INTO users (username, name, last_name, hash) VALUES (?, ?, ?, ?)", username, name, last_name, generate_password_hash(password_1))
        except:
            # If something goes wrong, means that the username has been taken
            warning = "Username already in use. Try another one"
            return render_template("register.html", warning=warning)
        
        # Save session
        session['user_id'] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]['id']
        
        return redirect("/homepage")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        # Define variables
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the user typed these two
        if not username or not password:
            warning = "Username and/or password not typed"
            return render_template("login.html", warning=warning)
        
        # Take out rows from the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check if the username exists and the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            warning = "Invalid username and/or password. Try again"
            return render_template("login.html", warning=warning)
        
        # Remember which user has logged in
        session['user_id'] = rows[0]['id']
        
        # Redirect to the homepage
        return redirect("/homepage")

@app.route("/")
@login_required
def homepage():
    # Get shit from the database
    # Get the pfp address from the database
    picture = db.execute('SELECT pfp FROM users WHERE id = ?', session['user_id'])[0]['pfp']

    # Compare the current weight with your goals
    prs = db.execute("SELECT exercise, weight FROM prs WHERE user_id = ?", session['user_id'])
    
    goals = db.execute("SELECT exercise, weight FROM goals WHERE user_id = ?", session['user_id'])
    
    progress = []
    # Assume that the prs recorded will always be in same quantity than the goals
    i = 0
    for goal in goals:
        weight = prs[i]['weight']
        progress.append({'exercise':goal['exercise'], 'diff': goal['weight'] - weight['weight']})
        i += 1        
    

    # Get the user's data
    user = db.execute("SELECT name, last_name FROM users WHERE id = ?", session['user_id'])[0]

    # Get routines class="register_button"
    routines = db.execute('SELECT routines.name, routines.description FROM routines INNER JOIN ids ON routines.id = ids.routine_id WHERE ids.user_id = ?', session['user_id'])

    return render_template("homepage.html", progress=progress, routines=routines, picture=picture, user=user)

@app.route("/routine", methods = ["GET", "POST"])
@login_required
def routine():
    if request.method == "POST":
        # TODO: Register the whole routine into the database
        # routine is now a list of Tuples that can't be edited
        routine = request.form

        # We start off with the basics, getting the name and description of the routine
        routine_name = routine.get('routine-name')
        routine_desc = routine.get('routine-desc')

        # Now, let's try to register each exercise
    else:
        # Show the page to register the routine
        return render_template("routine.html")
    