from app import app
from flask import Flask, render_template

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/register')
def register():
	return render_template('register.html')