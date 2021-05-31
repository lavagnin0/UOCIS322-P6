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


@app.route('/_req', methods=["POST"])
def req():
    format = flask.request.form.get('format')
    k = flask.request.form.get('k', default=0, type=int)
    if flask.request.form.get('check_open') and flask.request.form.get('check_close'):
        option = 'listAll'
    elif flask.request.form.get('check_open'):
        option = 'listOpenOnly'
    else:
        option = 'listCloseOnly'
    if format:
        url = API_URL + '/' + option + '/' + format + '?top=' + str(k)
        return redirect(url)
    else:
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
