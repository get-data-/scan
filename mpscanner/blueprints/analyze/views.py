from flask import (
    Blueprint,
    url_for,
    render_template,
    redirect,
    make_response,
    flash)
from mpscanner.blueprints.analyze.forms import CrawlForm, BulkCrawlForm
from mpscanner.extensions import mongo
from lib.potato.extract import name, websiteDomain
import pandas as pd
import uuid

analyze = Blueprint('analyze', __name__, template_folder='templates')


@analyze.route('/analyze/bulk', methods=['GET', 'POST'])
def bulk():
    form = BulkCrawlForm()
    if form.validate_on_submit():
        from mpscanner.blueprints.analyze.tasks import crawl
        urlgroup = str(form.websites.data).splitlines()
        batch_id = str(uuid.uuid1())
        for domain in urlgroup:
            crawl.delay(domain, batch_id=batch_id)
        flash('Domains sent off for analysis~!', 'success')
        return render_template('analyze/bulk.html', form=form)
    else:
        return render_template('analyze/bulk.html', form=form)


@analyze.route('/newreport/<job_id>/<report>/download')
def export(job_id, report):
    pageData = mongo.db.scan
    data = []
    if report == 'domain':
        for d in pageData.find({'uuid': job_id}):
            data.append(d['crawl_data'])
    elif report == 'batch':
        for d in pageData.find({'batch_id': job_id}):
            data.append(d['crawl_data'])
    df = pd.DataFrame(data)
    response = make_response(df.to_csv())
    response.headers['Content-Disposition'] = 'attachment; filename=export.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


@analyze.route('/newreports')
def scanReport():
    webData = mongo.db.scan
    data = []
    batch = []
    crawls = webData.aggregate(
        [{'$group': {'_id': {'homepage': '$homepage', 'uuid': '$uuid'}}}])
    batch_crawls = webData.distinct('batch_id')
    for d in crawls:
        data.append(d)
    for d in batch_crawls:
        batch.append(d)
    return render_template('analyze/new_reports.html', sites=data, batch=batch)


@analyze.route('/newreports/<site_id>')
def siteScanReport(site_id):
    pageData = mongo.db.scan
    data = []
    for d in pageData.find({'uuid': site_id}):
        data.append(d)
    return render_template('analyze/new_single_report.html', sites=data)


@analyze.route('/analyze', methods=['GET', 'POST'])
def index():
    company = mongo.db.trans
    form = CrawlForm()
    if form.validate_on_submit():
        url = websiteDomain(form.website.data)
        data = company.find_one({'website': url})
        if data:
            return redirect(url_for('analyze.analysis',
                            client=name(url)))
        else:
            from mpscanner.blueprints.analyze.tasks import crawl
            page = crawl.delay(url)
            # company.insert_one({'website': url, 'celery_id': page.id})
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
