import datetime
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine=create_engine('sqlite:///flask.db', echo=True)

# Create a sessionmaker
Session=sessionmaker(bind=engine)
session=Session()

users={"admin": "password", "charlie": "mingus", "lucile": "asdf"}

for user, password in users.items():	
	encrypted_pass=sha256_crypt.encrypt(password)
	current_user=User(user, encrypted_pass)
	session.add(current_user)

# Commit the record to the database
session.commit()