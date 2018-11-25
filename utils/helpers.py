import os


def read_dir(path):
    for dirname, dirnames, filenames in os.walk(path):
        return filenames


def read_file(file):
    with open(file) as f:
        content = f.read()
        return content


def gen_file_body(filename, content):
    return {
        'filename': filename,
        'content': content
    }


def gen_error_body(filename, errors):
    return {
        'filename': filename,
        'errors': errors
    }


def gen_warn_body(filename, warnings):
    return {
        'filename': filename,
        'warnings': warnings
    }


def gen_dir_body(dirname, content):
    return {
        'dirname': dirname,
        'content': content
    }