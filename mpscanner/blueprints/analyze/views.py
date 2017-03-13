from flask import (
    Blueprint,
    request,
    url_for,
    render_template,
    jsonify,
    redirect)

analyze = Blueprint('analyze', __name__, template_folder='templates')


@analyze.route('/analyze', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('analyze/index.html')
    return redirect(url_for('index'))


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
