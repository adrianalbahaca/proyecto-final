from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from login import login_required
from werkzeug.utils import secure_filename
import os

# Initialize the reception of files
UPLOAD_FOLDER = 'static/images/pfps'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        
        flash('Successfully logged in!')

        # Redirect to the homepage
        return redirect("/")
    
# Define function to return the most important data from the user
def get_user_data():
    user = dict()
    pfp = db.execute('SELECT pfp FROM users WHERE id = ?', session['user_id'])[0]['pfp']
    if not pfp == 'NULL':
        user['picture'] = None
    else:
        user['picture'] = UPLOAD_FOLDER + '/' + pfp
    user['name'] = db.execute("SELECT name FROM users WHERE id = ?", session['user_id'])[0]
    return user

@app.route("/")
@login_required
def homepage():
    # Get shit from the database
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

    # Get routines class="register_button"
    routines = db.execute('SELECT routines.name, routines.description FROM routines INNER JOIN ids ON routines.id = ids.routine_id WHERE ids.user_id = ?', session['user_id'])

    # Get the user's name and picture
    user = get_user_data()

    return render_template("homepage.html", progress=progress, routines=routines, picture=user['picture'], user=user['name'])

@app.route("/routine", methods = ["GET", "POST"])
@login_required
def routine():
    if request.method == 'POST':
        # TODO: Register the routine into the database and go back to the homepage
        # Register name and description of the routine
        routine = request.form.to_dict()
        name = routine['routine-name']
        desc = routine['routine-desc']

        # Create routine id in database
        db.execute('INSERT INTO ids (user_id) VALUES (?)', session['user_id'])

        # Get routine id
        id = db.execute('SELECT routine_id FROM ids WHERE user_id = ?', session['user_id'])[0]['routine_id']
        print(id)

        # Save routine into database
        db.execute('INSERT INTO routines (id, name, description) VALUES (?, ?, ?)', id, name, desc)

        # Now here comes the part where I need to think a lot...
        # Scroll through the dict and save each part into the database, using a counter
        # until it's the same to the length of the dict
        ex_c = 1
        
        # Scroll through the routine dict until there are no more exercises to show
        while True:
            # Try to register a new exercise
            try:
                exercise = routine['ex-name-'+ str(ex_c)]
            except:
                # If you can't register another exercise, then break this loop
                break
            
            set = 1
            # If not, means that this exercise exists
            for element in routine:
                # Get reps and weight
                try:
                    reps = routine['ex-'+ str(ex_c) +'-set-'+ str(set) +'-reps']
                    weight = routine['ex-'+ str(ex_c) +'-set-'+ str(set) +'-weight']
                except:
                    break   

                # Register the variables into the database
                db.execute('INSERT INTO routine_exercise (id, exercise, reps, weights) VALUES (?, ?, ?, ?)', id, exercise, reps, weight)

                # Increase set counter
                set += 1

            # Increase exercise counter
            ex_c += 1

        # Once the whole dict is registered, return to the homepage
        return redirect('/')

    else:
        user = get_user_data()
        return render_template('routine.html', user=user['name'], picture=user['picture'])
    
@app.route('/settings')
@login_required
def settings():
    user = get_user_data()
    return render_template('settings.html', user=user['name'], picture=user['picture'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    if request.method == 'GET':
        # Return the page to edit the profile picture
        user = get_user_data()
        return render_template('profile.html', user=user['name'], picture=user['picture'])
    else:
        # TODO: Receive the info given and update everything on the database

        # Start to save each thing up depending on what the person uploads
        name = request.form.get('new_name')
        if name:
            db.execute('UPDATE users SET name = ? WHERE id = ?', name, session['user_id'])

        username = request.form.get('new_username')
        if username:
            # Check if the username is in the database
            rows = db.execute('SELECT username FROM users WHERE username = ?', username)

            if len(rows) == 0:
                # If the length is equal to zero, it means that no one is using that username
                try:
                    db.execute('UPDATE users SET username = ? WHERE id = ?', username, session['user_id'])
                except:
                    flash('There was an issue while uploading your profile pic. Try again')
                    return redirect('/profile')
            else:
                # Else, the username is taken
                flash('The username is already taken. Try another one')
                return redirect('/profile')
        
        # Now for the pfp part (first time doing this Scheiße)
        if 'pfp' not in request.files:
            flash('No file part')
            return redirect('/profile')
        
        pfp = request.files['pfp']

        if pfp.filename == '':
            flash('No selected file')
            return redirect('/profile')
        
        if pfp and allowed_file(pfp.filename):
            pfp_name = secure_filename(pfp.filename)
            print(pfp_name)
            pfp.save(os.path.join(app.config['UPLOAD_FOLDER'], pfp_name))

            # Save to database
            db.execute('UPDATE users SET pfp = ? WHERE id = ?', pfp_name, session['user_id'])

        # Finally, returning to the settings page
        return redirect('/settings')

@app.route('/prs', methods = ['GET', 'POST'])
@login_required
def prs():
    if request.method == 'GET':
        # Return the page to edit the profile picture
        user = get_user_data()
        return render_template('prs.html', user=user['name'], picture=user['picture'])
    else:
        # TODO: Manage the PRs and save them into the database
        prs = request.form.to_dict()

        # Create some kind of loop that saves each exercise's name and weight into the database
        counter = 1
        while True:
            # Start by trying to register a new exercise
            try:
                pr_name = prs['ex-name-' + str(counter)]
                pr_weight = prs['ex-weight-' + str(counter)]
            except:
                # If it fails, then there's nothing else to register, so break the loop
                break

            # Save the name and weight into the database
            db.execute('INSERT INTO prs (user_id, exercise, weight) VALUES (?, ?, ?)', session['user_id'] , pr_name, pr_weight)

            # Increase counter by 1
            counter += 1
        flash('PRs successfully registered')
        return redirect('/settings')
    
@app.route("/password", methods = ['GET', 'POST'])
@login_required
def password():
    if request.method == 'GET':
        user = get_user_data()
        return render_template('password.html', user=user['name'], picture=user['picture'])
    else:
        # TODO: Change the password of the user
        old = request.form.get('old-password')
        new_1 = request.form.get('new-password-1')
        new_2 = request.form.get('new-password-2')

        # Check if the old password typed is the correct one
        if not check_password_hash(db.execute('SELECT hash FROM users WHERE id = ?', session['user_id'])[0]['hash'], old):
            flash('Incorrect password. Try again')
            return redirect('/password')
        
        # Check if the new passwords match
        if new_1 != new_2:
            flash("The new passwords don't match. Try again")
            return redirect('/password')
        
        # If everything is alright, then add the new password into the database
        hash = generate_password_hash(old)
        db.execute('UPDATE users SET hash = ? WHERE id = ?', hash, session['user_id'])

        flash('Password successfully changed')
        return redirect("/settings")

@app.route('/delete', methods = ['GET', 'POST'])
@login_required
def delete():
    if request.method == 'GET':
        user = get_user_data()
        return render_template('delete.html', user=user['name'], picture=user['picture'])
    else:
        # TODO: Delete the account and all of the info involved with it

        # Delete picture from the server
        picture = db.execute('SELECT pfp FROM users WHERE id = ?', session['user_id'])[0]['pfp']
        print(picture)
        if picture != None:
            file_path = UPLOAD_FOLDER + '/' + picture
            try:
                os.remove(file_path)
            except:
                flash('Something went wrong when trying to delete the profile picture')
                return redirect('/settings')
            
        print(session['user_id'])
        
        # Delete stuff from the 'routines' tables
        db.execute('DELETE FROM routines WHERE id = ?', session['user_id'])
        db.execute('DELETE FROM routine_exercise WHERE id = ?', session['user_id'])

        # Delete stuff from the 'ids' table
        db.execute('DELETE FROM ids WHERE user_id = ?', session['user_id'])

        # Delete stuff from the 'goals' and 'prs' tables
        db.execute('DELETE FROM goals WHERE user_id = ?', session['user_id'])
        db.execute('DELETE FROM prs WHERE user_id = ?', session['user_id'])

        # Delete info from the 'users' table
        db.execute('DELETE FROM users WHERE id = ?', session['user_id'])

        # Finally, close session
        session.clear()

        return redirect('/register')