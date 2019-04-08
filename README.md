# nexo-api-logs

1. [What's the point?](#whats-the-point)
2. [Logs resource](#logs-resource)
3. [Serve the Flask app for testing](#serve-the-flask-app-for-testing)
4. [Serve the Flask app as standalone WSGI container](#serve-the-flask-app-as-standalone-wsgi-container)
5. [What's next](#whats-next)


## What's the point?

* Simple project to expose endpoints.
* At this moments there is just a few services implemented about `logs` resource.

## Logs resource

Get the list of files within a directory.

```http request
GET /api/logs?dir=tests/resources
Accept: application/json
```

Get full content of `file.log`.

```http request
GET /api/logs?file=tests/resources/file.log
Accept: application/json
```

Get the content of `file.log` but just `INFO` traces.

```http request
GET /api/logs/info?file=tests/resources/file.log
Accept: application/json
```

Get the content of `file.log` but just `WARNING` traces.

```http request
GET /api/logs/warning?file=tests/resources/file.log
Accept: application/json
```

Get the content of `file.log` but just `ERROR` traces.

```http request
GET /api/logs/error?file=tests/resources/file.log
Accept: application/json
```

Get the content of `file.log` but just `ERROR` traces and only the last `3` lines.

```http request
GET /api/logs/error?file=tests/resources/file.log&nlines=3
Accept: application/json
```

Response

```http request
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 668
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Sun, 25 Nov 2018 12:56:34 GMT
```

```json
{
  "filename": "tests/resources/file.log",
  "errors": [
    "[2018-11-23 03:13:44,698][pipeline][ERROR]: 2 - Health failure on ['https://elastic-1.aws.cloud.es.io:9243']: http_status=502: 502 Server Error: Bad Gateway for url: https://elastic-1.aws.cloud.es.io:9243/_cluster/health",
    "[2018-11-23 03:13:47,331][pipeline][ERROR]: 3 - Health failure on ['https://elastic-1.aws.cloud.es.io:9243']: http_status=502: 502 Server Error: Bad Gateway for url: https://elastic-1.aws.cloud.es.io:9243/_cluster/health",
    "[2018-11-23 03:15:30,117][pipeline][ERROR]: 4 - Tags ingestion FAILED because too many failures: failures=`5`"
  ]
}
```


## Serve the Flask app for testing

Export env variables
```bash
export FLASK_APP=api.py
export FLASK_ENV=development
```

Activate virtual env
```bash
source ~/myenv/bin/activate 
```

Run Flask application
```bash
flask run
```


## Serve the Flask app as standalone WSGI container

We can serve the Flask application with a WSGI HTTP server. The easiest way is [Gunicorn](https://gunicorn.org/)

We have to install in our `venv`

```bash
pip install gunicorn
```

and serve as a daemon

```bash
gunicorn wsgi --bind 127.0.0.1:8921 --pid api.pid --daemon
```

To kill the server

```bash
kill $(cat api.pid)
```


## What's next

- [ ] Authorization
- [ ] Unit testing of each endpoint
- [ ] Create the `swagger.yaml`
- [ ] DockerFile
