from flask import Flask, request, render_template
from flask_restful import Resource, Api
import pymongo
from pymongo import MongoClient
import os
import flask

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

DEFAULT_SORT = [('dist', pymongo.ASCENDING)]


class ListAll(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        data = list(db.tododb.find({}, {'_id': 0, 'open': 1, 'close': 1}, sort=DEFAULT_SORT, limit=k))
        if dtype == 'csv':
            response = "Open,Close\n"
            for item in data:
                response += item['open'] + ',' + item['close'] + '\n'
            return reponse
        return flask.jsonify(data)


class ListOnlyOpen(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        data = list(db.tododb.find({}, {'_id': 0, 'open': 1}, sort=DEFAULT_SORT, limit=k))
        if dtype == 'csv':
            response = "Open\n"
            for item in data:
                response += item['open'] + '\n'
            return reponse
        return flask.jsonify(data)


class ListOnlyClose(Resource):
    def get(self, dtype=''):
        k = request.args.get('top', default=0, type=int)
        data = list(db.tododb.find({}, {'_id': 0, 'close': 1}, sort=DEFAULT_SORT, limit=k))
        if dtype == 'csv':
            response = "Close\n"
            for item in data:
                response += item['close'] + '\n'
            return reponse
        return flask.jsonify(data)


api.add_resource(ListAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(ListOnlyOpen, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(ListOnlyClose, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
