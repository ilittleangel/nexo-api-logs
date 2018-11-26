from api import application

"""
WSGI entrypoint for the application
"""
if __name__ == '__main__':
    application.run(debug=True)
