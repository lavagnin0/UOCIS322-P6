from flask import Flask, request, render_template
from flask_restful import Resource, Api
import pymongo
from pymongo import MongoClient
import os

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

DEFAULT_SORT = [('dist', pymongo.ASCENDING)]


class ListAll(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        if dtype == 'csv':
            pass
        return flask.jsonify(list(db.tododb.find({}, {'open': 1, 'close': 1}, sort=DEFAULT_SORT, limit=k)))


class ListOnlyOpen(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        if dtype == 'csv':
            pass
        return flask.jsonify(list(db.tododb.find({}, {'open': 1}, sort=DEFAULT_SORT, limit=k)))


class ListOnlyClose(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        if dtype == 'csv':
            pass
        return flask.jsonify(list(db.tododb.find({}, {'close': 1}, sort=DEFAULT_SORT, limit=k)))


api.add_resource(ListAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(ListOnlyOpen, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(ListOnlyClose, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
