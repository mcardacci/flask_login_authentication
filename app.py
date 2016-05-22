from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from passlib.hash import sha256_crypt
from sqlalchemy.orm import sessionmaker
from tabledef import *
import os

engine=create_engine("sqlite:///flask.db", echo=True)

app = Flask(__name__)

 
@app.route("/")
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		print session
		print session['user_id']
		return redirect(url_for('user_profile_page', user_id=session['user_id']))

@app.route('/login', methods=['POST'])
def login():
	POST_USERNAME=str(request.form['username'])
	POST_PASSWORD=str(request.form['password'])

	Session=sessionmaker(bind=engine)
	s=Session()
	query=s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
	result=query.first()
	# This is how to print a dict of an SQLAlchemy object
	# print result.__dict__
	# print result as a test and pass the id through url. here!
	if result:
		user_id=result.id
		username=result.username
		session['logged_in']=True
		session['user_id']=user_id
		session['username']=username
	else:
		flash('wrong username or password')
	return redirect(url_for('home'))


@app.route('/signup', methods=['GET'])
def signup():
	if session.get('logged_in'):
		flash('Please log out before signing up a new user.')
		return redirect(url_for('home'))
	else:
		return render_template('/signup.html')

@app.route("/profile", methods=['GET'])
def profile_page():
	return "Welcome Back! <a href='/logout'>Log Out</a>"	

@app.route("/profile/<int:user_id>", methods=['GET'])
def user_profile_page(user_id):
	user=session["username"]
	return "Welcome Back "+user+" <a href='/logout'>Log Out</a>"

@app.route("/logout")
def logout():
	session['logged_in']=False
	return redirect(url_for('home'))



#-------------------TESTING-------------------------------------
# How to write URL Params
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

# @app.route("/test")
# def test():
# 	POST_USERNAME="charlie"
# 	POST_PASSWORD="mingus"

# 	Session=sessionmaker(bind=engine)
# 	s=Session()
# 	query=s.query(User).filter(User.username.in_([POST_USERNAME]),User.password.in_([POST_PASSWORD]) )
# 	result=query.first()
# 	if result:
# 		return "Object Found"
# 	else:
# 		return "Object not found " + POST_USERNAME + " " + POST_PASSWORD

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
