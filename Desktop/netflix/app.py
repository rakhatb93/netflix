from flask import Flask, render_template, url_for, flash, redirect, request
import psycopg2
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.types import String
from forms import RegistrationForm, LoginForm
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = '2472345f7fa58ca28a92fb0b0adf9fa7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:199919991999r@localhost:5432/postgres'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}, '{self.email}')"

engine = create_engine('postgresql://postgres:199919991999r@localhost:5432/postgres')
df = pd.read_csv('netflix.csv')
sorted_csv_type = df.sort_values(['type', 'rating'])
sorted_csv_type.to_sql('sorted_netflix', engine, if_exists='replace', index=False, 
	dtype={"show_id": String(), "type": String(), "title": String(), "director": String(),
 "cast": String(), "country": String(), "date_added": String(), "release_year": String(),
 "rating": String(), "duration": String(), "listed_in": String(), "description": String()})

try:
	conn = psycopg2.connect(database="postgres", user="postgres", 
		password="199919991999r", host="localhost")
	print("Connected!")
except:
    print("Could not connect to database.")

mycursor = conn.cursor()   

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
	mycursor.execute("SELECT * FROM sorted_netflix")
	data = mycursor.fetchall()
	return render_template('home.html', data=data)	

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
    	hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    	user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    	db.session.add(user)
    	# db.session.commit()
    	flash('Your account has been created! You are now able to log in.', 'success')
    	return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    	  flash('You have been logged in', 'success')
    	  return redirect(url_for('home'))
    	else:
    	  flash('Login Unsuccessful. Please check username and password.')  
    return render_template('login.html', title='Login', form=form)

@app.route('/netflix', methods=['GET', 'POST'])
def netflix():
    ret    

if __name__ == '__main__':
    app.run(debug=True)    