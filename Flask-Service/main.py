from flask import Flask, g, request
from flask_restful import Resource, Api
from flask_cors import CORS
import couchdb

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return ([
            {"title": 'Carlton', "postCode": 3053},
            {"title": 'Brunswick', "postCode": 3053},
            {"title": 'Clayton', "postCode": 3053}
        ])


class Sample(Resource):
    def get(self):
        user = "admin"
        password = "admin"
        couchserver = couchdb.Server("http://%s:%s@172.26.133.34:5984/" % (user, password))
        for dbname in couchserver:
            dbname = "twitter"
            if dbname in couchserver:
                db = couchserver[dbname]
                # Create a view
                # Do the processing
                # return (result)
                return (db.get('51f39676462cca21859bd92d8e000f24'))

api.add_resource(HelloWorld, '/')
api.add_resource(Sample, '/getSample')

if __name__ == '__main__':
    app.run(debug=True)