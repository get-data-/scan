from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators


class CrawlForm(Form):
    website = StringField(u'Enter a website', [
        validators.required(),
        validators.URL(require_tld=True, message=u'Invalid URL.')])


class BulkCrawlForm(Form):
    websites = TextAreaField(
        u'List of domains to analyze',
        [validators.optional(), validators.length(max=30000)])
