import pytz
import datetime
from textblob import TextBlob
import re
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


def get_sentiment_score_vaccine_df():
    score_df = pd.read_csv('sentiment_score_vaccine.csv')
    score_df_dict = {}
    for index, row in score_df.iterrows():
        score_df_dict[str(row['id'])] = None
    couchserver = couchdb.Server(
        "http://%s:%s@172.26.133.161:5984/" % (user, password))
    db = couchserver['raw_tweets_from_timeline']
    vaccine_tweets_id_view = db.view('vaccine_related/Vaccine_tweets_id')
    keys = []
    for r in vaccine_tweets_id_view:
        if r.key not in score_df_dict:
            keys.append(r.key)
    vaccine_tweets_view_result = db.view('vaccine_related/Vaccine_tweets', keys=keys)
    sentiment_score_vaccine = {}
    for r in vaccine_tweets_view_result:
        sentiment_score_vaccine[r.key] = r.value
    for key in sentiment_score_vaccine.keys():
        tweet_info = sentiment_score_vaccine[key]
        tweet_info.append(get_tweet_sentiment_score_textblob(
            sentiment_score_vaccine[key][2]))
    time_created = []
    location = []
    full_text = []
    score_textblob = []
    week = []
    start_date = datetime.datetime(2020, 1, 1).replace(
        tzinfo=pytz.timezone('Australia/Sydney'))
    end_date = (start_date + datetime.timedelta(days=7)
                ).replace(tzinfo=pytz.timezone('Australia/Sydney'))

    for key in sentiment_score_vaccine.keys():
        time_converted = convert_to_time(sentiment_score_vaccine[key][0])
        if (time_converted - end_date).days >= 0:
            end_date = end_date + datetime.timedelta(days=7)
        time_created.append(time_to_str(time_converted))
        week.append(time_to_str(end_date))
        location.append(sentiment_score_vaccine[key][1])
        full_text.append(sentiment_score_vaccine[key][2])
        score_textblob.append(sentiment_score_vaccine[key][3])

    sentiment_score_vaccine_df = pd.DataFrame(
        {'id': sentiment_score_vaccine.keys(), 'time_created': time_created, 'location': location, 'full_text': full_text, 'score_textblob': score_textblob, 'week': week})
    return score_df.append(sentiment_score_vaccine_df)


def clean_tweet(tweet):
    '''
    Cleans tweet text by removing links, users mentioned, special characters and emojis - using regex statements.

    '''
    return ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(@[A-Za-z0-9]+)", " ", tweet).split())


def get_tweet_sentiment_score_textblob(tweet):
    '''
    Returns textual sentiment score of tweet, taken from polarity using textblob's sentiment method, 
    a float within the range [-1.0, 1.0] ranging from very negative to very positive.

    '''
    # Create TextBlob object of passed tweet textblob
    analysis = TextBlob(clean_tweet(tweet))

    return analysis.sentiment.polarity


def convert_to_time(time_str):
    return datetime.datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=pytz.timezone('Australia/Sydney'))


def time_to_str(t):
    return datetime.datetime.strftime(t, "%Y-%m-%d")


class Cities(Resource):
    def get(self):
        return ([
            {"label": 'Melbourne', "value": "melbourne"},
            {"label": 'Adelaide', "value": "adelaide"},
            {"label": 'Sydney', "value": "sydney"},
            {"label": 'Canberra', "value": "canberra"},
            {"label": 'Darwin', "value": "darwin"},
            {"label": 'Hobart', "value": "hobart"},
            {"label": 'Perth', "value": "perth"},
            {"label": 'Brisbane', "value": 'brisbane'}
        ])


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

    # Read the covid cases dataset
    covid_cases_statedate = get_view(
        "covid_cases",
        "state_cases",
        "StateConfirmedCases_sum",
        4,
        'true'
    )

    # Function for adding the confirmed cases in each state in particular time to the city list
    covid_tweet_citymonth = get_view(
        "raw_tweets_from_timeline",
        "covid_related",
        "CityDateTime_count",
        4,
        'true'
    )

    def get(self):
        city = request.args['city']
        data = []

        for row in self.covid_cases_statedate:
            datetime = [row["key"][1], row["key"][2], row["key"][3]]
            datetime = "-".join(str(e).zfill(2) for e in datetime)
            if(row["key"][0] == self.cityStateMap[city]):
                if row["value"] >= 0:
                    data.append(
                        {
                            "time": datetime,
                            "cases": row["value"]
                        }
                    )

        for i in range(len(data)):
            for row in self.covid_tweet_citymonth:
                datetime = [row["key"][1], row["key"][2], row["key"][3]]
                datetime = "-".join(str(e).zfill(2) for e in datetime)
                if data[i]["time"] == datetime and row["key"][0] == city:
                    data[i]["tweets"] = row["value"]
                    break
                else:
                    data[i]["tweets"] = 0

        return data


class CovidGraph3(Resource):
    def get(self):
        data = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        wordcloud_covid_view_result = db.view(
            'covid_related/Wordcloud_covid', group=True)
        stop_words = stopwords.words('english')
        stop_words_manual1 = ['covid19', 'covid', 'coronavirus', 'amp', 'get', 'getting', 'got', 'one', 'two', '1', '2', '3', '4', 'via', 'like', 'would',
                              'still', 'could', 'it’s', 'go', 'going', '…', 'may', 'also', 'even', 'take', 'make', 'way', 'dont', 'don’t', 'cant', 'im', 'i’m', 'around', '–']
        word_count_covid = {}
        for r in wordcloud_covid_view_result:
            if r.key not in stop_words and r.key != '' and r.key not in stop_words_manual1:
                word_count_covid[r.key] = r.value
        for word in ['vaccine', 'vaccination', 'health', 'government', 'lockdown', 'know', 'risk', 'test', 'spread', 'response', 'live', 'help', 'support', 'hotel', 'travel', 'million', 'hospital', 'outbreak']:
            word_count_covid[word] = word_count_covid[word] + \
                word_count_covid[word+'s']
            word_count_covid[word+'s'] = 0

        for word in ['cases', 'deaths', 'restrictions', 'patients', 'workers', 'masks', 'symptoms']:
            word_count_covid[word] = word_count_covid[word] + \
                word_count_covid[word[:-1]]
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
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
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


class CovidMap(Resource):
    def get(self):
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
        # couchserver = couchdb.Server(
        #     "http://%s:%s@172.26.133.161:5984/" % (user, password))
        # db = couchserver['raw_tweets_from_timeline']
        covid_tweet_citymonth = get_view(
            "raw_tweets_from_timeline",
            "covid_related",
            "CityDateTime_count",
            3,
            'true'
        )
        covid_tweet_citymonth_dict = {}
        max_count = 0
        for r in covid_tweet_citymonth:
            # get max count
            if r.value > max_count:
                max_count = r.value
            # use YYYY-MM as the key, add tweet count of each city to the dictionary
            key = str(r.key[1]) + '-' + str(r.key[2])
            if key not in covid_tweet_citymonth_dict:
                covid_tweet_citymonth_dict[key] = [{'name':cityStateMap[r.key[0]], 'value': r.value}]
            else:
                covid_tweet_citymonth_dict[key].append({'name':cityStateMap[r.key[0]], 'value': r.value})
        data = []
        # sort the date
        dates = sorted(covid_tweet_citymonth_dict.keys(), key = lambda item: (int(item.split('-')[0]), int(item.split('-')[1])))
        for date in dates:
            info_by_date = {
                'date': date,
                'tweet_count_data': covid_tweet_citymonth_dict[date]
            }
            data.append(info_by_date)
        return {'max_count': max_count, 'data': data}


class CovidGetTweetByHashtag(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word'][1:]
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        for item in db.view('covid_related/Wordcloud_hashtag_covid', include_docs=True, key=word, reduce=False, limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0, len(contents) - 1)
        return contents[random_index]


class CovidGetTweetByWord(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word']
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('covid_related/Wordcloud_covid', include_docs=True, key=word, reduce=False, limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0, len(contents) - 1)
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
        sentiment_score_vaccine_df = get_sentiment_score_vaccine_df()
        score_by_date = sentiment_score_vaccine_df.groupby(by=['week'])
        score_mean = score_by_date.mean()['score_textblob']
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


class VaccineGraph3(Resource):
    def get(self):
        sentiment_score_vaccine_df = get_sentiment_score_vaccine_df()
        score_by_location = sentiment_score_vaccine_df.groupby(by=['location'])
        score_mean = score_by_location.mean()['score_textblob']
        data = []
        for index in score_mean.index:
            data_location = {
                'avg sentiment score': round(score_mean[index], 4),
                'city': index,
            }
            data.append(data_location)

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


class VaccineGraph4(Resource):
    def get(self):
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        wordcloud_vaccine_view_result = db.view(
            'vaccine_related/Wordcloud_vaccine', group=True)
        stop_words = stopwords.words('english')
        stop_words_manual2 = ['vaccine','vaccines','vaccinated','vaccinate','vaccination','vaccinations','amp','get','getting','got','say','one','two','1','2','3','4','50','via','like','would','still','could','it’s','go','going','…','may','also','even','take','make','made','way','dont','don’t','cant','im','i’m','around','–','yet','much','give','given','every','thats','another','without']
        word_count_vaccine = {}
        for r in wordcloud_vaccine_view_result :
            if r.key not in stop_words and r.key != '' and r.key not in stop_words_manual2:
                word_count_vaccine[r.key] = r.value
        for word in ['australia','health','government','morrison','quarantine','know','think','risk','million','work','flu','jab','mrna','program','pfizer','astrazeneca','moderna']:
            word_count_vaccine[word] = word_count_vaccine[word] + word_count_vaccine[word+'s']
            word_count_vaccine[word+'s'] = 0
            
        for word in ['doses','cases','deaths','australians','workers','clots']:
            word_count_vaccine[word] = word_count_vaccine[word] + word_count_vaccine[word[:-1]]
            word_count_vaccine[word[:-1]] = 0
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
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        data = []
        wordcloud_vaccine_view_result = db.view(
            'vaccine_related/Wordcloud_hashtag_vaccine', group=True)
        word_count_vaccine_hashtag = {}
        stop_words = stopwords.words('english')
        for r in wordcloud_vaccine_view_result:
            word = r.key
            word = '#' + word.lower()
            if word not in stop_words and word != '' and word not in ['#vaccine','#vaccines','#vaccination']:
                if word not in word_count_vaccine_hashtag.keys():
                    word_count_vaccine_hashtag[word] = r.value
                else:
                    word_count_vaccine_hashtag[word] += r.value

        word_count_vaccine_hashtag = sorted(word_count_vaccine_hashtag.items(
        ), key=lambda item: item[1], reverse=True)[:50]
        for item in word_count_vaccine_hashtag:
            data.append({
                'text':  item[0],
                'value': item[1]
            })
        return data


class VaccineGetTweetByHashtag(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word'][1:]
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('vaccine_related/Wordcloud_hashtag_vaccine', include_docs=True, key=word, reduce=False, limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0, len(contents) - 1)
        return contents[random_index]


class VaccineGetTweetByWord(Resource):
    def post(self):
        word = json.loads(request.get_data(as_text=True))['word']
        contents = []
        couchserver = couchdb.Server(
            "http://%s:%s@172.26.133.161:5984/" % (user, password))
        db = couchserver['raw_tweets_from_timeline']
        for item in db.view('covid_related/Wordcloud_covid', include_docs=True, key=word, reduce=False, limit=100):
            contents.append(item.doc['full_text'])
        random_index = random.randint(0, len(contents) - 1)
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
api.add_resource(CovidMap, '/api/covid/map')
api.add_resource(CovidGetTweetByHashtag,
                 '/api/covid/hashtag/get_tweet_by_word')
api.add_resource(CovidGetTweetByWord, '/api/covid/get_tweet_by_word')
# api.add_resource(CovidWordCloudData, '/api/getCovidWordCloudData')

api.add_resource(VaccineGraph1, '/api/vaccine/getGraph1Data')
api.add_resource(VaccineGraph2, '/api/vaccine/sentiment_trend')
api.add_resource(VaccineGraph3, '/api/vaccine/getGraph3Data')
api.add_resource(VaccineGraph4, '/api/vaccine/words_cloud')
api.add_resource(VaccineGraph5, '/api/vaccine/hashtag/words_cloud')
api.add_resource(VaccineGetTweetByHashtag,
                 '/api/vaccine/hashtag/get_tweet_by_word')
api.add_resource(VaccineGetTweetByWord, '/api/vaccine/get_tweet_by_word')

api.add_resource(JobGraph1, '/api/job-keeper/getGraph1Data')
api.add_resource(JobGraph2, '/api/job-keeper/getGraph2Data')
api.add_resource(JobGraph3, '/api/job-keeper/getGraph3Data')

if __name__ == '__main__':
    app.run(debug=True)
