from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class CrawlForm(Form):
    website = StringField(u'Enter a website', [
        validators.required(),
        validators.URL(require_tld=True, message=u'Invalid URL.')])
