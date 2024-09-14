from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from login import login_required
from werkzeug.utils import secure_filename
import os

# Initialize the reception of files
UPLOAD_FOLDER = 'static/images/pfps/'
ALLOWED_EXTENSIONS = {'.png', '.jpeg', '.jpg'}

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize sessions so as to use filesystems
app.config["SESSION PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure that responses aren't cached
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
        password_1 = request.form.get('password-1')
        password_2 = request.form.get('password-2')

        # Check if any of the variables are mission
        if not username or not password_1 or not password_2 or not name:
            flash("Missing passwords, full name and/or email. Try again")
            return redirect('/register')
        
        # Check if the passwords match
        if password_1 != password_2:
            flash("Passwords don't match")
            return redirect('/register')
        
        # Try to insert the username, email and passwords into the database
        try:
            db.execute("INSERT INTO users (username, name, hash) VALUES (?, ?, ?)", username, name, generate_password_hash(password_1))
        except:
            # If something goes wrong, means that the username has been taken
            flash('Username already taken. Try another one')
            return redirect('/register')
        
        # Save session
        session['user_id'] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]['id']
        
        flash('Successfully registered')
        return redirect("/")

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
            flash('Username and/or password not typed in')
            return redirect('/login')
        
        # Take out rows from the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check if the username exists and the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash('Incorrect password. Try again')
            return redirect('/login')
        
        # Remember which user has logged in
        session['user_id'] = rows[0]['id']
        
        flash('Successfully logged in!')

        # Redirect to the homepage
        return redirect("/")
    
# Define function to return the most important data from the user
def get_user_data():
    user = dict()
    pfp = db.execute('SELECT pfp FROM users WHERE id = ?', session['user_id'])[0]['pfp']
    if pfp == 'NULL':
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
    routines = db.execute('SELECT routines.name, routines.description, routines.id FROM routines INNER JOIN ids ON routines.id = ids.routine_id WHERE ids.user_id = ?', session['user_id'])

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

        db.execute('INSERT INTO ids (user_id) VALUES (?)', session['user_id'])
        id = db.execute('SELECT routine_id FROM ids WHERE user_id = ?', session['user_id'])[0]['routine_id']
        db.execute('INSERT INTO routines (id, name, description) VALUES (?, ?, ?)', id, name, desc)
        
        # TODO: Create a loop that saves each set, reps and weight of each exercise
        # Create a counter and scroll through the routine dict
        c = 1

        while True:
            try:
                # Try to register a new exercise
                exercise = routine['ex-name-' + str(c)]
            except:
                # If you can't do it, it means there are no more exercises to register
                break
            # If all goes well, we look for each set
            s = 1
            for elements in routine:
                # We're gonna use the elements in the 'routine' dict as a counter
                try:
                    reps = routine['ex-' + str(c) + '-set-' + str(s) + '-reps']
                    weight = routine['ex-' + str(c) + '-set-' + str(s) + '-weight']
                except:
                    # If they didn't find the reps and weight of a set, there's no more
                    break
                
                # If they found the info, register the info
                db.execute('INSERT INTO routine_exercise (id, exercise, reps, weights) VALUES (?, ?, ?, ?)', id, exercise, reps, weight)
                # Increase the set counter
                s += 1
            
            # Increase the exercise counter
            c += 1

        return redirect('/')

    else:
        user = get_user_data()
        return render_template('routine.html', user=user['name'], picture=user['picture'])
    
@app.route('/routine-check', methods=['GET', 'POST'])
@login_required
def routine_check():
    if request.method == 'POST':
        id = request.form.get('routine-id')

        # Get the name and description of the routine from the database
        routine_data = db.execute('SELECT id, name, description FROM routines WHERE id = ?', id)

        # Get each exercise from the routine
        values = db.execute('SELECT exercise, reps, weights FROM routine_exercise WHERE id = ?', id)
        for value in values:
            routine_data.append(value)
        
        l = len(routine_data)
        
        print(routine_data)
        # Return template with the routine list
        return render_template('routine-check.html', routine=routine_data, len=l)
    
@app.route('/routine-delete', methods = ['POST'])
@login_required
def routine_delete():
    d = request.form.get('routine-id')

    # Delete all the data on the database
    db.execute('DELETE FROM routines WHERE id = ?', d)
    db.execute('DELETE FROM routine_exercise WHERE id = ?', d)
    db.execute('DELETE FROM ids WHERE routine_id = ?', d)

    # Flash a message
    flash('Routine successfully deleted')

    return redirect('/')
    
@app.route('/settings')
@login_required
def settings():
    user = get_user_data()
    return render_template('settings.html', user=user['name'], picture=user['picture'])

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
        pfp = request.files['pfp']
        extension = os.path.splitext(pfp.filename)[1]
        print(extension)

        if pfp:
            if extension not in ALLOWED_EXTENSIONS:
                flash('The profile pic is not an image. Upload a JPG or PNG image')
                return redirect('/profile')
            else:
                pfp.save(os.path.join(
                    UPLOAD_FOLDER, secure_filename(pfp.filename)
                ))
                db.execute('UPDATE users SET pfp = ? WHERE id = ?', pfp.filename, session['user_id'])
        
        # Finally, returning to the settings page
        return redirect('/settings')

@app.route('/prs', methods = ['GET', 'POST'])
@login_required
def prs():
    if request.method == 'GET':
        # Return the page to edit the profile picture
        user = get_user_data()
        prs = db.execute('SELECT exercise, weight, date FROM prs WHERE user_id = ?', session['user_id'])
        return render_template('prs.html', user=user['name'], picture=user['picture'], prs=prs)
    else:
        # TODO: Manage the PRs and save them into the database
        exercise = request.form.get('pr-exercise')
        weight = request.form.get('pr-weight')
        date = request.form.get('pr-date')

        db.execute('INSERT INTO prs (user_id, exercise, weight, date) VALUES (?, ?, ?, ?)', session['user_id'], exercise, weight, date)

        return redirect('/prs')
    
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