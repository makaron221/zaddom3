from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import sqlite3

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    replypassword = PasswordField('reply password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods =['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if "@" in form.email.data:
            conn = sqlite3.connect('database.db')
            loginn = ""
            for i in form.email.data:
                if i != '@':
                    loginn += i
                else:
                    break
            conn.execute('INSERT INTO accounts VALUES(?, ?, ?)',(form.email.data, loginn, form.password.data))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
            
    return render_template('register.html', form=form)
    
@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('database.db')
        if conn.execute("SELECT password FROM accounts WHERE login = ?", (form.login.data,)).fetchone()[0] == form.password.data:
            return "you are logged into your account"
    return render_template('login.html', form=form)
