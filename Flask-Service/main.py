from flask import Flask, g, request
from flask_restful import Resource, Api, request
from flask_cors import CORS
import couchdb

app = Flask(__name__)
# cors = CORS(app)
api = Api(app)


class Cities(Resource):
    def get(self):
        return ([
            {"label": 'Melbourne', "value": 1},
            {"label": 'Adelaide', "value": 2},
            {"label": 'Sydney', "value": 3}
        ])


class Sample(Resource):
    def get(self):
        user = "admin"
        password = "admin"
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.34:5984/" % (user, password))
        for dbname in couchserver:
            dbname = "twitter"
            if dbname in couchserver:
                db = couchserver[dbname]
                # Create a view
                # Do the processing
                # return (result)
                return (db.get('51f39676462cca21859bd92d8e000f24'))


class CovidGraph1(Resource):
    def get(self):
        return ([
            {"name": "Melbourne", "remaining": 1000, "covid": 335},
            {"name": "Brisbane", "remaining": 1000, "covid": 345},
            {
                "name": "Perth",
                "remaining": 1000,
                "covid": 2110
            },
            {
                "name": "Adelaide",
                "remaining": 1000,
                "covid": 540
            },
            {
                "name": "Hobart",
                "remaining": 1000,
                "covid": 335
            },
            {"name": "Darwin", "remaining": 1000, "covid": 110},
            {"name": "Canberra", "remaining": 1000, "covid": 110}
        ])


class CovidGraph2(Resource):
    def get(self):
        print(request.args['city'])
        return ([
            {
                "name": "1/01/2021",
                "tweets": 4000,
                "cases": 2400,
            },
            {
                "name": "2/01/2021",
                "tweets": 3000,
                "cases": 1398,
            },
            {
                "name": "3/01/2021",
                "tweets": 2000,
                "cases": 9800,
            },
            {
                "name": "4/01/2021",
                "tweets": 2780,
                "cases": 3908,
            },
            {
                "name": "5/01/2021",
                "tweets": 1890,
                "cases": 4800,
            },
            {
                "name": "6/01/2021",
                "tweets": 2390,
                "cases": 3800,
            },
            {
                "name": "7/01/2021",
                "tweets": 3490,
                "cases": 4300,
            }
        ])


class CovidWordCloudData(Resource):
    def get(self):
        return ([
            {
                "text": 'word1',
                "value": 64,
            },
            {
                "text": 'word2',
                "value": 11,
            },
            {
                "text": 'word3',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            },
            {
                "text": 'Covid',
                "value": 64,
            },
            {
                "text": 'mistake',
                "value": 11,
            },
            {
                "text": 'thought',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            }, {
                "text": 'Covid',
                "value": 64,
            },
            {
                "text": 'mistake',
                "value": 11,
            },
            {
                "text": 'thought',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            }, {
                "text": 'Covid',
                "value": 64,
            },
            {
                "text": 'mistake',
                "value": 11,
            },
            {
                "text": 'thought',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            },
            {
                "text": 'told',
                "value": 64,
            },
            {
                "text": 'mistake',
                "value": 11,
            },
            {
                "text": 'thought',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            },
            {
                "text": 'Covid',
                "value": 64,
            },
            {
                "text": 'mistake',
                "value": 11,
            },
            {
                "text": 'thought',
                "value": 16,
            },
            {
                "text": 'bad',
                "value": 17,
            },
        ])


api.add_resource(Cities, '/getCities')
api.add_resource(CovidGraph1, '/getCovidGraph1Data')
api.add_resource(CovidGraph2, '/getCovidGraph2Data')
api.add_resource(CovidWordCloudData, '/getCovidWordCloudData')
api.add_resource(Sample, '/getSample')

if __name__ == '__main__':
    app.run(debug=True)
