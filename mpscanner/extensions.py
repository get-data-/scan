from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf import CsrfProtect
from flask_pymongo import PyMongo

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CsrfProtect()
db = PyMongo()
