import flask
from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_URL = 'http://{}:{}'.format(os.environ['RESTAPI_HOSTNAME'], os.environ['RESTAPI_PORT'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/_req')
def req():
    format = flask.request.form.get('format', default='json', type=str)
    k = flask.request.form.get('k', default=0, type=int)
    open = flask.request.form.get('check_open', default='', type=str)
    close = flask.request.form.get('check_close', default='', type=str)
    if open and close:
        option = 'listAll'
    elif open:
        option = 'listOpenOnly'
    else:
        option = 'listCloseOnly'
    url = API_URL + '/' + option + '/' + format + '?top=' + str(k)
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
