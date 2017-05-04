from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf import CsrfProtect
from flask_pymongo import PyMongo
# from mongokit import Connection

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CsrfProtect()
mongo = PyMongo()
# db = Connection()
