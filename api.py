from flask import Flask, request, Response, url_for, jsonify
import os
import json

app = Flask(__name__)


def _read_dir(path):
    for dirname, dirnames, filenames in os.walk(path):
        return filenames


def _read_file(file):
    with open(file) as f:
        content = f.read()
        return content


def _gen_file_body(filename, content):
    return {
        'filename': filename,
        'content': content
    }


def _gen_error_body(filename, errors):
    return {
        'filename': filename,
        'errors': errors
    }


def _gen_warn_body(filename, warnings):
    return {
        'filename': filename,
        'warnings': warnings
    }


def _gen_dir_body(dirname, content):
    return {
        'dirname': dirname,
        'content': content
    }


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
    if 'file' in request.args:
        body = _gen_file_body(request.args['file'], _read_file(request.args['file']))
        status = 200
    elif 'dir' in request.args:
        body = _gen_dir_body(request.args['dir'], _read_dir(request.args['dir']))
        status = 200
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=status, mimetype='application/json')
    return res


def _gen_response(level):
    if 'file' in request.args:
        filename = request.args['file']
        n_lines = request.args.get('nlines', default=2)
        lines = [line for line in _read_file(filename).splitlines() if level in line.lower()][-n_lines]
        if level == 'error':
            body = _gen_error_body(filename, errors=lines)
        elif level == 'warning':
            body = _gen_warn_body(filename, warnings=lines)
        else:
            return error404(f'Not Found: resource does not exits: {request.url}')
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=200, mimetype='application/json')
    return res


@app.route('/api/logs/info', methods=['GET'])
def logs_info():
    if 'file' in request.args:
        filename = request.args['file']
        n_lines = request.args.get('nlines', default=2)
        infos = [line for line in _read_file(filename).splitlines() if "info" in line.lower()][-n_lines]
        body = _gen_error_body(filename, infos)
        status = 200
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=status, mimetype='application/json')
    return res


@app.route('/api/logs/error', methods=['GET'])
def logs_error():
    if 'file' in request.args:
        filename = request.args['file']
        n_lines = request.args.get('nlines', default=2)
        errors = [line for line in _read_file(filename).splitlines() if "error" in line.lower()][-n_lines]
        body = _gen_error_body(filename, errors)
        status = 200
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=status, mimetype='application/json')
    return res


@app.route('/api/logs/warning', methods=['GET'])
def logs_warning():
    if 'file' in request.args:
        filename = request.args['file']
        n_lines = request.args.get('nlines', default=2)
        warnings = [line for line in _read_file(filename).splitlines() if "warning" in line.lower()][-n_lines]
        body = _gen_warn_body(filename, warnings)
        status = 200
    else:
        return error404(f'Not Found: resource does not exits: {request.url}')

    res = Response(json.dumps(body, indent=4), status=status, mimetype='application/json')
    return res


if __name__ == '__main__':
    app.run(debug=True)
