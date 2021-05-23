from flask import Flask, g, request, jsonify
from flask_restful import Resource, Api, request
from flask_cors import CORS
import couchdb
import json
import pandas as pd
import random
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


app = Flask(__name__)
cors = CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


user = "admin"
password = "admin"

def get_view(db_name, doc_name, view_name, group_level=0, reduce='false'):
    user = "admin"
    password = "admin"
    couchserver = couchdb.Server(
        "http://%s:%s@172.26.133.161:5984/" % (user, password))
    db = couchserver[db_name]
    return db.view(name=doc_name + '/' + view_name, group_level=group_level, reduce=reduce)


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


# class Sample(Resource):
#     def get(self):
#         user = "admin"
#         password = "admin"
#         couchserver = couchdb.Server(
#             "http://%s:%s@172.26.133.34:5984/" % (user, password))
#         for dbname in couchserver:
#             dbname = "twitter"
#             if dbname in couchserver:
#                 db = couchserver[dbname]
#                 # Create a view
#                 # Do the processing
#                 # return (result)
#                 return (db.get('51f39676462cca21859bd92d8e000f24'))


class CovidGraph1(Resource):
    def get(self):

        data = []

        # Count the number of tweets mentioned covid in each city
        covid_tweet_city = get_view(
            db_name="raw_tweets_from_timeline",
            doc_name="covid_related",
            view_name="CityDateTime_count",
            group_level=1,
            reduce='true')

        for row in covid_tweet_city:
            data.append({
                "city": row["key"][0],
                "metioned_covid": row["value"]
            })

        # Count the total number of tweets in each city
        tweet_city = get_view(
            db_name="raw_tweets_from_timeline",
            doc_name="covid_related",
            view_name="Tweet_count",
            group_level=1,
            reduce='true'
        )

        for row in tweet_city:
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        return data


class CovidGraph2(Resource):

    data = []
    case_state = {}

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

    # Function for adding the number of tweets mentioned covid in particular city and time to the city list
    def add_value(self, key, value):
        Scenario_two_temp = {"time": {}, "tweets": {}}
        Datetime = [key[1], key[2], key[3]]
        Scenario_two_temp["time"] = "-".join(str(e).zfill(2) for e in Datetime)
        Scenario_two_temp["tweets"] = value
        self.data.append(Scenario_two_temp)

    #  Function for adding the confirmed cases in each state in particular time to the city list

    def add_case(self):
        for i in range(len(self.data)):
            if self.data[i]["time"] in set(self.case_state.keys()):
                casesCount = self.case_state[self.data[i]["time"]]
                casesCount = 0 if casesCount < 0 else casesCount
                self.data[i]["cases"] = casesCount

    def get(self):
        city = request.args['city']

        covid_cases_statedate = get_view(
            "covid_cases",
            "state_cases",
            "StateConfirmedCases_sum",
            4,
            'true'
        )

        for row in covid_cases_statedate:
            Datetime = [row["key"][1], row["key"][2], row["key"][3]]
            Date_time = "-".join(str(e).zfill(2) for e in Datetime)
            if(row["key"][0] == self.cityStateMap[city]):
                self.case_state[Date_time] = row["value"]

        # Read the number of tweets mentioned covid group/aggregated by location, year, month, date
        covid_tweet_citydate = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "CityDateTime_count",
            4,
            'true'
        )

        # Add the number of tweets mentioned covid and date to each city list
        for row in covid_tweet_citydate:
            if city == row["key"][0]:
                self.add_value(row["key"], row["value"])

        # Add the confirmed cases info to each city list
        self.add_case()

        return self.data


class CovidGraph3(Resource):
    def get(self):
        data = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        wordcloud_covid_view_result = db.view(
            'covid_related/Wordcloud_covid', group=True)
        stop_words = stopwords.words('english')
        stop_words_manual1 = ['covid19','covid','coronavirus','amp','get','getting','got','one','two','1','2','3','4','via','like','would','still','could','it’s','go','going','…','may','also','even','take','make','way','dont','don’t','cant','im','i’m','around','–']
        word_count_covid = {}
        for r in wordcloud_covid_view_result :
            if r.key not in stop_words and r.key != '' and r.key not in stop_words_manual1:
                word_count_covid[r.key] = r.value
        for word in ['vaccine','vaccination','health','government','lockdown','know','risk','test','spread','response','live','help','support','hotel','travel','million','hospital','outbreak']:
            word_count_covid[word] = word_count_covid[word] + word_count_covid[word+'s']
            word_count_covid[word+'s'] = 0
            
        for word in ['cases','deaths','restrictions','patients','workers','masks','symptoms']:
            word_count_covid[word] = word_count_covid[word] + word_count_covid[word[:-1]]
            word_count_covid[word[:-1]] = 0
        # get top 80 results
        word_count_covid = sorted(word_count_covid.items(
        ), key=lambda item: item[1], reverse=True)[:80]
        for item in word_count_covid:
            data.append({
                'text': item[0],
                'value': item[1]
            })

        return data


class CovidGraph4(Resource):
    def get(self):
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        wordcloud_covid_view_result = db.view(
            'covid_related/Wordcloud_hashtag_covid', group=True)
        word_count_covid = {}
        for r in wordcloud_covid_view_result:
            if r.key not in ['covid19', 'covid', 'coronavirus', 'covid_19', 'covidー19']:
                word_count_covid[r.key] = r.value
        word_count_covid = sorted(word_count_covid.items(
        ), key=lambda item: item[1], reverse=True)[:60]
        for item in word_count_covid:
            data.append({
                'text': '#' + item[0],
                'value': item[1]
            })
        return data

class CovidGetTweetByHashtag(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word'][1:]
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        for item in db.view('covid_related/Wordcloud_hashtag_covid',include_docs=True,key=word, reduce=False,limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0,len(contents) - 1)
        return contents[random_index]

class CovidGetTweetByWord(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word']
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('covid_related/Wordcloud_covid',include_docs=True,key=word, reduce=False,limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0,len(contents) - 1)
        return contents[random_index]

class VaccineGraph1(Resource):
    def get(self):
        data = []

        # Count the number of tweets mentioned vaccine in each city
        vaccine_tweet_city = get_view(
            "raw_tweets_from_timeline",
            "vaccine_related",
            "Vaccine_CityDateTime_count",
            1,
            'true'
        )

        for row in vaccine_tweet_city:
            data.append(
                {
                    "city": row["key"][0],
                    "metioned_vaccine": row["value"]
                }
            )

        # Count the total number of tweets in each city
        tweet_city = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "Tweet_count",
            1,
            'true'
        )

        for row in tweet_city:
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        return data


class VaccineGraph2(Resource):
    def get(self):
        score_df = pd.read_csv('sentiment_score_vaccine.csv')
        score_by_date = score_df.groupby(by=['week'])
        score_mean = score_by_date.mean()['score_textblob']
        score_median = score_by_date.quantile(0.5)['score_textblob']
        score_quantile10 = score_by_date.quantile(0.1)['score_textblob']
        score_quantile90 = score_by_date.quantile(0.9)['score_textblob']
        data = []
        for index in score_mean.index:
            data_day = {
                'value': round(score_mean[index], 4),
                'date': index,
                'range': [round(score_quantile10[index], 4), round(score_quantile90[index], 4)]
            }
            data.append(data_day)
        return data


class VaccineGraph4(Resource):
    def get(self):
        vaccine_words = ['covid19', 'covid', 'people', 'pfizer', 'australia', 'rollout', 'astrazeneca', 'us', 'doses', 'government', 'need', 'az', 'health', 'australians', 'first', 'new', 'risk', 'know', 'million', 'time', 'many', 'virus', 'think', 'good', 'cases', 'says', 'world', 'auspol', 'well', 'morrison', 'jab', 'work', 'coronavirus', 'year', 'deaths', 'quarantine', 'want', 'see', 'said', 'care', 'countries', 'news', 'workers', 'immunity', 'effective', 'scottmorrisonmp', '7news',
                         'mrna', 'flu', 'blood', 'week', 'clots', 'uk', 'enough', 'public', 'data', 'back', 'govt', 'months', 'next', 'last', 'right', 'program', 'everyone', 'safe', 'available', 'use', 'better', 'day', 'really', 'already', 'aged', 'end', 'moderna', 'federal', 'country', 'today', 'medical', 'long', 'population', 'greghuntmp', 'stop', 'states', 'pandemic', 'open', 'never', 'years', 'sure', 'point', 'days', 'minister', 'must', 'weeks', 'keep', 'roll', 'yes', 'wait', 'borders', 'due', 'india']
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        wordcloud_vaccine_view_result = db.view(
            'vaccine_related/Wordcloud_vaccine', group=True, keys=vaccine_words)
        word_count_vaccine = {}
        for r in wordcloud_vaccine_view_result:
            word_count_vaccine[r.key] = r.value
        # get top 80 results
        word_count_vaccine = sorted(word_count_vaccine.items(
        ), key=lambda item: item[1], reverse=True)[:80]
        for item in word_count_vaccine:
            data.append({
                'text':  item[0],
                'value': item[1]
            })
        return data


class VaccineGraph5(Resource):
    def get(self):
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        wordcloud_vaccine_view_result = db.view(
            'vaccine_related/Wordcloud_hashtag_vaccine', group=True)
        word_count_vaccine = {}
        for r in wordcloud_vaccine_view_result:
            word_count_vaccine[r.key] = r.value
        word_count_vaccine = sorted(word_count_vaccine.items(
        ), key=lambda item: item[1], reverse=True)[:50]
        for item in word_count_vaccine:
            data.append({
                'text': '#' + item[0],
                'value': item[1]
            })
        return data

class VaccineGetTweetByHashtag(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word'][1:]
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('vaccine_related/Wordcloud_hashtag_vaccine',include_docs=True,key=word, reduce=False,limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0,len(contents) - 1)
        return contents[random_index]

class VaccineGetTweetByWord(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word']
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.246:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('covid_related/Wordcloud_covid',include_docs=True,key=word, reduce=False,limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0,len(contents) - 1)
        return contents[random_index]

class JobGraph1(Resource):
    def get(self):
        data = []

        job_tweet_city = get_view(
            "raw_tweets_from_timeline",
            "job_related",
            "Job_CityDateTime_count",
            1,
            'true'
        )

        for row in job_tweet_city:
            data.append({
                "city": row["key"][0],
                "metioned_jobkeeper": row["value"]
            })

        tweet_city = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "Tweet_count",
            1,
            'true'
        )

        for row in tweet_city:
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        income_info = get_view(
            "aurin_income",
            "income_doc",
            "income"
        )

        for row in income_info:
            for i in range(len(data)):
                if(row['key'] == '40070' and data[i]["city"] == 'adelaide'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '31000' and data[i]["city"] == 'brisbane'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '89399' and data[i]["city"] == 'canberra'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '71000' and data[i]["city"] == 'darwin'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '62810' and data[i]["city"] == 'hobart'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '24600' and data[i]["city"] == 'melbourne'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '57080' and data[i]["city"] == 'perth'):
                    data[i]['median_weekly_personal_income'] = row['value']
                elif(row['key'] == '17200' and data[i]["city"] == 'sydney'):
                    data[i]['median_weekly_personal_income'] = row['value']

        return data


class JobGraph2(Resource):
    def get(self):
        data = []

        job_tweet_city = get_view(
            "raw_tweets_from_timeline",
            "job_related",
            "Job_CityDateTime_count",
            1,
            'true'
        )

        for row in job_tweet_city:
            if row["key"][0] != "canberra":
                data.append({
                    "city": row["key"][0],
                    "metioned_jobkeeper": row["value"]
                })

        tweet_city = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "Tweet_count",
            1,
            'true'
        )

        for row in tweet_city:
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        jobseeker_payment_info = get_view(
            "aurin_quarterly_payment",
            "JobseekerPayment_doc",
            "quarterly_payment"
        )

        for row in jobseeker_payment_info:
            for i in range(len(data)):
                if(row['key'] == '40070' and data[i]["city"] == 'adelaide'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '31000' and data[i]["city"] == 'brisbane'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '89399' and data[i]["city"] == 'canberra'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '71000' and data[i]["city"] == 'darwin'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '62810' and data[i]["city"] == 'hobart'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '24600' and data[i]["city"] == 'melbourne'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '57080' and data[i]["city"] == 'perth'):
                    data[i]['jobseeker_payment'] = row['value']
                elif(row['key'] == '17200' and data[i]["city"] == 'sydney'):
                    data[i]['jobseeker_payment'] = row['value']

        return data


class JobGraph3(Resource):
    def get(self):
        data = []

        job_tweet_city = get_view(
            "raw_tweets_from_timeline",
            "job_related",
            "Job_CityDateTime_count",
            1,
            'true'
        )

        for row in job_tweet_city:
            if row["key"][0] != "canberra":
                data.append({
                    "city": row["key"][0],
                    "metioned_jobkeeper": row["value"]
                })

        tweet_city = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "Tweet_count",
            1,
            'true'
        )

        for row in tweet_city:
            for i in range(len(data)):
                if row["key"] == data[i]["city"]:
                    data[i]["total_tweets"] = row["value"]

        aged_info = get_view(
            "aurin_regional_population",
            "Aged_15_64_doc",
            "Aged_15_64"
        )

        for row in aged_info:
            for i in range(len(data)):
                if(row['key'] == '40070' and data[i]["city"] == 'adelaide'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '31000' and data[i]["city"] == 'brisbane'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '89399' and data[i]["city"] == 'canberra'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '71000' and data[i]["city"] == 'darwin'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '62810' and data[i]["city"] == 'hobart'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '24600' and data[i]["city"] == 'melbourne'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '57080' and data[i]["city"] == 'perth'):
                    data[i]['Aged_15_64_percentage'] = row['value']
                elif(row['key'] == '17200' and data[i]["city"] == 'sydney'):
                    data[i]['Aged_15_64_percentage'] = row['value']

        return data


api.add_resource(Cities, '/api/getCities')

api.add_resource(CovidGraph1, '/api/covid/getGraph1Data')
api.add_resource(CovidGraph2, '/api/covid/getGraph2Data')
api.add_resource(CovidGraph3, '/api/covid/words_cloud')
api.add_resource(CovidGraph4, '/api/covid/hashtag/words_cloud')
api.add_resource(CovidGetTweetByHashtag, '/api/covid/hashtag/get_tweet_by_word')
api.add_resource(CovidGetTweetByWord, '/api/covid/get_tweet_by_word')
# api.add_resource(CovidWordCloudData, '/api/getCovidWordCloudData')

api.add_resource(VaccineGraph1, '/api/vaccine/getGraph1Data')
api.add_resource(VaccineGraph2, '/api/vaccine/sentiment_trend')
api.add_resource(VaccineGraph4, '/api/vaccine/words_cloud')
api.add_resource(VaccineGraph5, '/api/vaccine/hashtag/words_cloud')
api.add_resource(VaccineGetTweetByHashtag, '/api/vaccine/hashtag/get_tweet_by_word')
api.add_resource(VaccineGetTweetByWord, '/api/vaccine/get_tweet_by_word')

api.add_resource(JobGraph1, '/api/job-keeper/getGraph1Data')
api.add_resource(JobGraph2, '/api/job-keeper/getGraph2Data')
api.add_resource(JobGraph3, '/api/job-keeper/getGraph3Data')

if __name__ == '__main__':
    app.run(debug=True)
