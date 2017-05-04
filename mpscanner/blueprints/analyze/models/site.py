# from mpscanner.extensions import mongo
# from mpscanner.extensions import db, Document
# import datetime
#
#
# @db.register
# class Website(Document):
#     __collection__ = 'site'
#     __database__ = 'belly'
#     structure = {
#         'domain_name': basestring,
#         'html': basestring,
#         'response': int,
#         'url': basestring,
#         'visit_date': datetime.datetime,
#         'rendered_by': basestring
#     }
#     required_fields = ['domain_name', 'html', 'response', 'url', 'visit_date']
#     default_values = {
#         'visit_date': datetime.datetime.utcnow
#     }

# class Analysis(db.Model):
