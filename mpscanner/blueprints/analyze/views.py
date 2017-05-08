from flask import (
    Blueprint,
    request,
    url_for,
    render_template,
    jsonify,
    redirect)
from mpscanner.blueprints.analyze.forms import CrawlForm
from mpscanner.extensions import mongo
from lib.potato.extract import name

analyze = Blueprint('analyze', __name__, template_folder='templates')


@analyze.route('/analyze', methods=['GET', 'POST'])
def index():
    company = mongo.db.trans
    form = CrawlForm()
    if form.validate_on_submit():
        from urllib.parse import urlparse
        website = urlparse(form.website.data)
        url = '%s://%s' % (website.scheme, website.netloc)
        data = company.find_one({'website': url})
        if data:
            return redirect(url_for('analyze.analysis',
                            client=name(url)))
        else:
            from mpscanner.blueprints.analyze.tasks import crawl
            page = crawl.delay(url)
            company.insert_one({'website': url, 'celery_id': page.id})
            return render_template('analyze/index.html', data=page, form=form)
    else:
        return render_template('analyze/index.html', form=form)


@analyze.route('/sitestatus/<task_id>', methods=['GET', 'POST'])
def sitestatus(task_id):
    form = CrawlForm()
    from mpscanner.blueprints.analyze.tasks import crawl
    results = crawl.AsyncResult(task_id)
    if results.ready():
        return render_template('analyze/index.html',
                               form=form, data=results.get())
    else:
        return redirect(url_for('analyze.index'))


@analyze.route('/reports')
def reporting():
    onelink = mongo.db.onelink
    data = []
    for d in onelink.find():
        company = d['domain_name']
        data.append(company)
    data.sort()
    return render_template('analyze/reports.html', data=data)


@analyze.route('/reports/<client>')
def analysis(client):
    company = mongo.db.trans
    data = company.find_one({'domain_name': client})
    return render_template('analyze/clientReport.html', data=data)


@analyze.route('/reports/<client>/translation')
def translation(client):
    company = mongo.db.trans
    data = []
    results = company.find({'domain_name': client})
    for r in results:
        data.append(r)
    return render_template('analyze/translation.html', data=data)


@analyze.route('/reports/<client>/seo')
def seo(client):
    company = mongo.db.trans
    data = company.find_one({'domain_name': client})
    return render_template('analyze/seo.html', data=data)


@analyze.route('/reports/<client>/products')
def products(client):
    company = mongo.db.trans
    data = company.find_one({'domain_name': client})
    return render_template('analyze/mpreport.html', data=data)
