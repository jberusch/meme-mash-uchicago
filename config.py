import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'do-this-later'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # if True, signals application every time a change is about to be made to the DB
        # may be useful in the future
    SQLALCHEMY_TRACK_MODIFICATIONS = False