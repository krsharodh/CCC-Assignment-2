from flask import Flask, g, request
from flask_restful import Resource, Api, request
from flask_cors import CORS
import couchdb
import requests
import json
import pandas as pd
import csv

app = Flask(__name__)
cors = CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


user = "admin"
password = "admin"


def get_view(db_name, doc_name, view_name, group_level):
    return requests.get(f"http://{user}:{password}@172.26.133.161:5984/{db_name}/_design/{doc_name}/_view/{view_name}?reduce=true&group_level={group_level}")


class Cities(Resource):
    def get(self):
        return ([
            {"label": 'Melbourne', "value": "melbourne"},
            {"label": 'Adelaide', "value": "adelaide"},
            {"label": 'Sydney', "value": "sydney"},
            {"label": 'Canberra', "value": "canberra"},
            {"label": 'Darwin', "value": "darwin"},
            {"label": 'Hobart', "value": "hobart"},
            {"label": 'Perth', "value": "perth"}
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

        data = []

        # Count the number of tweets mentioned covid in each city
        covid_tweet_city = json.loads(
            get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="CityDateTime_count",
                group_level=1
            ).content.decode("utf-8"))

        for row in covid_tweet_city['rows']:
            # print(row["key"], row["value"])
            data.append({
                "city": row["key"][0],
                "metioned_covid": row["value"]
            })

        # Count the total number of tweets in each city
        tweet_city = json.loads(
            get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="Tweet_count",
                group_level=1
            ).content.decode("utf-8"))

        for row in tweet_city['rows']:
            # print(row["key"], row["value"])
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        # print(data)

        return data


class CovidGraph2(Resource):

    data = []
    case_state = None

    cityStateMap = {
        "adelaide": "SA",
        "brisbane": "QLD",
        "canberra": "ACT",
        "darwin": "NT",
        "hobart": "TAS",
        "melbourne": "VIC",
        "perth": "WA",
        "sydney": "NSW",
    }

    def add_value(self, key, value):
        Scenario_two_temp = {"time": {}, "tweets": {}}
        Datetime = [key[1], key[2] + 1, key[3] + 1]
        Scenario_two_temp["time"] = "-".join(str(e).zfill(2) for e in Datetime)
        Scenario_two_temp["tweets"] = value
        self.data.append(Scenario_two_temp)

    #  Function for adding the confirmed cases in each state in particular time to the city list
    def add_case(self):
        for i in range(len(self.data)):
            if self.data[i]["time"] in set(self.case_state.date):
                index = self.case_state[self.case_state['date'] ==
                                        self.data[i]["time"]].index.values[0]
                casesCount = int(self.case_state.at[index, 'confirmed'])
                casesCount = 0 if casesCount < 0 else casesCount
                self.data[i]["cases"] = casesCount

    def get(self):
        city = request.args['city']

        with open('COVID_AU_state_daily_change.csv', newline='') as f:
            reader = csv.reader(f)
            case = pd.DataFrame(reader)
            new_header = case.iloc[0]
            case = case[1:]
            case.columns = new_header

            # Create a series of lists to store the confirmed cases information for each state
            self.case_state = case.loc[case['state_abbrev']
                                       == self.cityStateMap[city]]

        # Read the number of tweets mentioned covid group/aggregated by location, year, month, date
        covid_tweet_citymonth = json.loads(
            get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="CityDateTime_count",
                group_level=4
            ).content.decode("utf-8"))

        # Add the number of tweets mentioned covid and date to each city list
        for row in covid_tweet_citymonth['rows']:
            if city == row["key"][0]:
                self.add_value(row["key"], row["value"])

        # Add the confirmed cases info to each city list
        self.add_case()

        return self.data


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
