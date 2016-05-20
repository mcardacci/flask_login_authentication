import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine=create_engine('sqlite:///flask.db', echo=True)

# Create a sessionmaker
Session=sessionmaker(bind=engine)
session=Session()

user=User("admin", "password")
session.add(user)

user=User("charlie", "mingus")
session.add(user)

user=User("lucile", "asdf")
session.add(user)

# Commit the record to the database
session.commit()