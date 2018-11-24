import os


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