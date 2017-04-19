from flask import (
    Blueprint,
    request,
    url_for,
    render_template,
    jsonify,
    redirect)
from mpscanner.blueprints.analyze.forms import CrawlForm
from mpscanner.extensions import mongo


analyze = Blueprint('analyze', __name__, template_folder='templates')


@analyze.route('/analyze', methods=['GET', 'POST'])
def index():
    company = mongo.db.trans
    form = CrawlForm()
    if form.validate_on_submit():
        url = form.website.data
        data = company.find_one({'website': url})
        if data:
            return redirect(url_for('analyze.analysis',
                            client=data['domain_name']))
        else:
            print('no data')
        return render_template('analyze/index.html', data=url, form=form)
    else:
        return render_template('analyze/index.html', form=form)


@analyze.route('/longtask', methods=['POST'])
def longtask():
    from mpscanner.blueprints.analyze.tasks import long_task
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('analyze.taskstatus',
                                                  task_id=task.id)}


@analyze.route('/status/<task_id>')
def taskstatus(task_id):
    from mpscanner.blueprints.analyze.tasks import long_task
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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
