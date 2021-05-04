from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

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


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
