import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL 


# Database name --  fyurrdb
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:petertalk@localhost:5434/fyurrdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False 


