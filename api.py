from flask import Flask, request, Response, jsonify
import json
import os

from utils.helpers import read_file, gen_file_body, gen_error_body, gen_warn_body
from utils.logging import init_logging
from settings import ROOT_DIR


application = Flask(__name__)
init_logging(application, f'{ROOT_DIR}/logs/api.log')

not_found_msg = 'Not found the `file=` pathParam inside the queryString'
not_such_file = 'No such file or directory'


@application.route('/api/logs', methods=['GET'])
def logs():
    application.logger.debug(f"{request.args}")
    if 'file' not in request.args:
        return not_found(not_found_msg)

    filename = request.args['file']
    if not os.path.isfile(filename):
        return not_found(not_such_file)
    body = gen_file_body(filename, list(read_file(filename).splitlines()))

    res = Response(json.dumps(body, indent=4), status=200, mimetype='application/json')
    return res


def _gen_response(level):
    application.logger.debug(f"{request.args}")
    if 'file' not in request.args:
        return not_found(not_found_msg)

    filename = request.args['file']
    n_lines = request.args.get('nlines', type=int)
    if not os.path.isfile(filename):
        return not_found(not_such_file)

    # full content
    lines = [line for line in read_file(filename).splitlines() if f'[{level.upper()}]' in line]
    if n_lines:
        # only n last lines
        length = len(lines)
        lines = lines[length-n_lines:length]

    if level == 'info':
        body = gen_file_body(filename, content=lines)
    elif level == 'error':
        body = gen_error_body(filename, errors=lines)
    elif level == 'warning':
        body = gen_warn_body(filename, warnings=lines)
    else:
        return not_found(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=200, mimetype='application/json')
    return res


@application.route('/api/logs/info', methods=['GET'])
def logs_info():
    return _gen_response('info')


@application.route('/api/logs/error', methods=['GET'])
def logs_error():
    return _gen_response('error')


@application.route('/api/logs/warning', methods=['GET'])
def logs_warning():
    return _gen_response('warning')


@application.errorhandler(404)
def not_found(msg):
    message = {
        'code': 404,
        'reason': 'notFound',
        'message': f'{msg}'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
