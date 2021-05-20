from flask import Flask, g, request
from flask_restful import Resource, Api, request
from flask_cors import CORS
import couchdb
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
    user = "admin"
    password = "admin"
    couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))
    db = couchserver[db_name]
    return db.view(name = doc_name + '/' + view_name, group_level = group_level, reduce='true')


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
        covid_tweet_city = get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="CityDateTime_count",
                group_level=1
            )

        for row in covid_tweet_city['rows']:
            # print(row["key"], row["value"])
            data.append({
                "city": row["key"][0],
                "metioned_covid": row["value"]
            })

        # Count the total number of tweets in each city
        tweet_city = get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="Tweet_count",
                group_level=1
            )

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
        covid_tweet_citymonth = get_view(
                db_name="raw_tweets_from_timeline",
                doc_name="covid_related",
                view_name="CityDateTime_count",
                group_level=4
            )

        # Add the number of tweets mentioned covid and date to each city list
        for row in covid_tweet_citymonth['rows']:
            if city == row["key"][0]:
                self.add_value(row["key"], row["value"])

        # Add the confirmed cases info to each city list
        self.add_case()

        return self.data


class CovidWordCloudData(Resource):
    def get(self):
        return ([{'text': 'covid19', 'value': 1814}, {'text': 'covid', 'value': 1657}, {'text': 'people', 'value': 1476}, {'text': 'pfizer', 'value': 1398}, {'text': 'australia', 'value': 1117}, {'text': 'dose', 'value': 908}, {'text': 'astrazeneca', 'value': 897}, {'text': 'us', 'value': 794}, {'text': 'million', 'value': 781}, {'text': 'rollout', 'value': 698}, {'text': 'new', 'value': 641}, {'text': 'health', 'value': 630}, {'text': 'risk', 'value': 626}, {'text': 'year', 'value': 614}, {'text': 'az', 'value': 608}, {'text': 'case', 'value': 540}, {'text': 'good', 'value': 532}, {'text': 'first', 'value': 517}, {'text': 'government', 'value': 494}, {'text': 'death', 'value': 489}, {'text': 'news', 'value': 483}, {'text': 'virus', 'value': 481}, {'text': 'give', 'value': 477}, {'text': 'world', 'value': 476}, {'text': 'countries', 'value': 465}, {'text': 'time', 'value': 454}, {'text': 'variant', 'value': 449}, {'text': '7news', 'value': 430}, {'text': 'uk', 'value': 430}, {'text': 'work', 'value': 425}, {'text': 'auspol', 'value': 418}, {'text': 'week', 'value': 415}, {'text': 'well', 'value': 407}, {'text': 'effective', 'value': 401}, {'text': 'coronavirus', 'value': 392}, {'text': 'immunity', 'value': 372}, {'text': 'trial', 'value': 364}, {'text': 'efficacy', 'value': 360}, {'text': 'cases', 'value': 352}, {'text': 'dose', 'value': 350}, {'text': 'going', 'value': 348}, {'text': 'want', 'value': 348}, {'text': 'work', 'value': 331}, {'text': 'much', 'value': 325}, {'text': 'data', 'value': 320}, {'text': 'mrna', 'value': 319}, {'text': 'see', 'value': 312}, {'text': 'use', 'value': 311}, {'text': 'better', 'value': 304}, {'text': 'population', 'value': 303}, {'text': 'got', 'value': 302}, {'text': 'blood', 'value': 301}, {'text': 'stop', 'value': 298}, {'text': 'safe', 'value': 293}, {'text': 'go', 'value': 284}, {'text': 'say', 'value': 278}, {'text': 'deaths', 'value': 277}, {'text': 'flu', 'value': 275}, {'text': 'yet', 'value': 275}, {'text': 'already', 'value': 274}, {'text': 'says', 'value': 270}, {'text': 'everyone', 'value': 269}, {'text': 'public', 'value': 265}, {'text': 'country', 'value': 264}, {'text': 'right', 'value': 264}, {'text': 'jab', 'value': 263}, {'text': 'australian', 'value': 262}, {'text': 'way', 'value': 262}, {'text': 'australians', 'value': 260}, {'text': 'end', 'value': 260}, {'text': 'said', 'value': 259}, {'text': 'back', 'value': 252}, {'text': 'years', 'value': 251}, {'text': 'long', 'value': 247}, {'text': 'next', 'value': 246}, {'text': 'morrison', 'value': 242}, {'text': 'herd', 'value': 241}, {'text': 'administered', 'value': 240}, {'text': 'quarantine', 'value': 234}, {'text': 'care', 'value': 230}, {'text': 'india', 'value': 228}, {'text': 'infection', 'value': 227}])


api.add_resource(Cities, '/getCities')
api.add_resource(CovidGraph1, '/getCovidGraph1Data')
api.add_resource(CovidGraph2, '/getCovidGraph2Data')
api.add_resource(CovidWordCloudData, '/getCovidWordCloudData')
api.add_resource(Sample, '/getSample')

if __name__ == '__main__':
    app.run(debug=True)
