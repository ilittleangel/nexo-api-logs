from flask import Flask, request, Response, jsonify
import json

from settings import ROOT_DIR
from utils.helpers import read_dir, read_file, gen_file_body, gen_error_body, gen_warn_body, gen_dir_body
from utils.logging import init_logging


app = Flask(__name__)
init_logging(app, f'{ROOT_DIR}/logs/api.log')


@app.errorhandler(404)
def error404(msg):
    message = {
        'code': 404,
        'reason': 'notFound',
        'message': f'{msg}'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/api/logs', methods=['GET'])
def logs():
    app.logger.debug(f"{request.args}")
    if 'file' in request.args:
        body = gen_file_body(request.args['file'], read_file(request.args['file']))
        status = 200
    elif 'dir' in request.args:
        body = gen_dir_body(request.args['dir'], read_dir(request.args['dir']))
        status = 200
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=status, mimetype='application/json')
    return res


def _gen_response(level):
    if 'file' in request.args:
        app.logger.debug(f"{request.args}")
        filename = request.args['file']
        n_lines = request.args.get('nlines', type=int)

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
            return error404(f'Not Found: resource does not exits: {request.url}')
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=200, mimetype='application/json')
    return res


@app.route('/api/logs/info', methods=['GET'])
def logs_info():
    return _gen_response('info')


@app.route('/api/logs/error', methods=['GET'])
def logs_error():
    return _gen_response('error')


@app.route('/api/logs/warning', methods=['GET'])
def logs_warning():
    return _gen_response('warning')


if __name__ == '__main__':
    app.run(debug=True)
