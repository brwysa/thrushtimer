from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Email
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import email_validator
import sqlite3


app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY'] ="o6#|'U7n#A;*y:"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}')"

class Task(db.Model): 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sessions = db.Column(db.Integer)
    complete =db.Column(db.Boolean, default=0)

class Pomodoro(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    work = db.Column(db.Integer, nullable=False)
    short_break = db.Column(db.Integer, nullable=False)
    long_break = db.Column(db.Integer, nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has been taken. Please choose a different one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has been taken. Please choose a different one!')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign in')


@app.route('/login',  methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Incorrect email or password!')
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/register',  methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! Please log in.')
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    username = current_user.username
    user_id = current_user.id

    exists = cur.execute("SELECT work FROM pomodoro WHERE user_id = ?", [user_id]).fetchall()

    if exists == []:
        duration = "INSERT INTO pomodoro (user_id, work, short_break, long_break) VALUES (?, ?, ?, ?)"
        data = (user_id, 20, 5, 15)
        cur.execute(duration, data)
            
        # Save (commit) the changes
        con.commit()
   
    # Fetch the data
    # cur.execute("SELECT work, short_break, long_break FROM pomodoro WHERE user_id = ?", [user_id])
    cur.execute("SELECT work FROM pomodoro WHERE user_id = ?", [user_id])
    workduration = cur.fetchall()
    timer = str(workduration).strip('[]').strip('()').strip(',')
    work = int(timer)

    cur.execute("SELECT short_break FROM pomodoro WHERE user_id = ?", [user_id])
    shortduration = cur.fetchall()
    shorttimer = str(shortduration).strip('[]').strip('()').strip(',')
    short = int(shorttimer)

    cur.execute("SELECT long_break FROM pomodoro WHERE user_id = ?", [user_id])
    longduration = cur.fetchall()
    longtimer = str(longduration).strip('[]').strip('()').strip(',')
    long = int(longtimer)
    return render_template("index.html", username=username, work=work, short=short, long=long)


@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")


@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    user_id = current_user.id

    if request.method == "POST":
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        workDuration = request.form.get("work")
        shortDuration = request.form.get("shortBreak")
        longDuration = request.form.get("longBreak")

        # Insert a row of data
        exists = cur.execute("SELECT work FROM pomodoro WHERE user_id = ?", [user_id]).fetchall()

        if exists == []:
            duration = "INSERT INTO pomodoro (user_id, work, short_break, long_break) VALUES (?, ?, ?, ?)"
            data = (user_id, workDuration, shortDuration, longDuration)
            cur.execute(duration, data)
        
            # Save (commit) the changes
            con.commit()

        else: 
            cur.execute("UPDATE pomodoro SET work = ?, short_break = ?, long_break = ?", [workDuration, shortDuration, longDuration])
        
            # Save (commit) the changes
            con.commit()

        return render_template("setting.html")

    else:
        return render_template("setting.html")


@app.route("/project", methods=["GET", "POST"])
@login_required
def project():
    user_id = current_user.id

    if request.method == "POST":
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        title = request.form.get("task-title")
        description = request.form.get("task-description")
        sessions = request.form.get("num-of-sessions")

        # Insert a row of data
        new_task = "INSERT INTO task (user_id, title, description, sessions, complete) VALUES (?, ?, ?, ?, ?)"
        data = (user_id, title, description, sessions, 0)
        cur.execute(new_task, data)
        # Save (commit) the changes
        con.commit()

        # Fetch the data
        cur.execute("SELECT title, description, sessions, id, complete FROM task WHERE user_id = ?", [user_id])
        tasks = cur.fetchall()
        sum_task = len(tasks)

        return render_template("project.html", tasks=tasks, len=sum_task)

    else:
        con = sqlite3.connect('database.db')
        cur = con.cursor()
    
        cur.execute("SELECT title, description, sessions, id, complete FROM task WHERE user_id = ?", [user_id])
        tasks = cur.fetchall()

        sum_task = len(tasks)
        return render_template("project.html", tasks=tasks, len=sum_task)

@app.route("/update/<int:task_id>")
def update(task_id):
    #update task status
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    if task.sessions == 0:
        task.sessions = 1
    db.session.commit()
    return redirect(url_for("project"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    #delete task
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("project"))

@app.route("/plus/<int:task_id>")
def plus(task_id):
    #add session
    task = Task.query.filter_by(id=task_id).first()
    task.sessions += 1
    db.session.commit()
    return redirect(url_for("project"))

@app.route("/minus/<int:task_id>")
def minus(task_id):
    #reduce session
    task = Task.query.filter_by(id=task_id).first()
    task.sessions -= 1
    if task.sessions == 0:
        task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("project"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
