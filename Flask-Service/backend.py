from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import *
import pandas as pd
import json
import couchdb
import random
from nltk.corpus import stopwords
import nltk
import re
from textblob import TextBlob
nltk.download('stopwords')

user = "admin"
password = "admin"
couchserver = couchdb.Server("http://%s:%s@172.26.133.246:5984/" % (user, password))
db = couchserver['raw_tweets_from_timeline']

app = Flask(__name__)
CORS(app, supports_credentials=True)

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
   return datetime.datetime.strptime(time_str,"%a %b %d %H:%M:%S %z %Y").replace(tzinfo=pytz.timezone('Australia/Sydney'))

def time_to_str(t):
   return datetime.datetime.strftime(t,"%Y-%m-%d")

def convert_city_to_stat(city):
   city_to_state = {
      'sydney': 'NSW',
      'melbourne': 'VIC',
      'brisbane': 'QLD',
      'adelaide': 'SA',
      'canberra': 'ACT',
      'hobart': 'Tasmania',
      'perth': 'WA',
      'darwin': 'NT'
   }
   return city_to_state[city]

@app.route('/vaccine/sentiment_score',methods = ['POST', 'GET'])
def vaccine_sentiment_score():
   # sentiment_score_vaccine = {}
   # for r in db.view('vaccine_related/Vaccine_tweets'):
   #    sentiment_score_vaccine[r.key] = [r.value['created_at'], r.value['uniform_location'], r.value['full_text']]
   # for key in sentiment_score_vaccine.keys():
   #    tweet_info = sentiment_score_vaccine[key]
   #    tweet_info.append(get_tweet_sentiment_score_textblob(sentiment_score_vaccine[key][2]))
   # time_created = []
   # location = []
   # full_text = []
   # score_textblob = []
   # week = []
   # start_date = datetime.datetime(2020,1,1).replace(tzinfo=pytz.timezone('Australia/Sydney'))
   # end_date = (start_date + datetime.timedelta(days=7)).replace(tzinfo=pytz.timezone('Australia/Sydney'))

   # for key in sentiment_score_vaccine.keys():
   #    time_converted = convert_to_time(sentiment_score_vaccine[key][0])
   #    if (time_converted - end_date).days >= 0:
   #       end_date = end_date + datetime.timedelta(days=7)
   #    time_created.append(time_to_str(time_converted))
   #    week.append(time_to_str(end_date))
   #    location.append(sentiment_score_vaccine[key][1])
   #    full_text.append(sentiment_score_vaccine[key][2])
   #    score_textblob.append(sentiment_score_vaccine[key][3])

   # sentiment_score_vaccine_df = pd.DataFrame(
   #    {
   #       'id':sentiment_score_vaccine.keys(), 
   #       'time_created':time_created, 
   #       'location':location, 
   #       'full_text':full_text, 
   #       'score_textblob':score_textblob,
   #       'week':week
   #    }
   # )
   data = []
   score_df = pd.read_csv('backend/sentiment_score_vaccine.csv')
   score_vaccine_by_location = score_df.groupby(by = ['location'])
   score_mean = score_vaccine_by_location.mean()['score_textblob']
   for index in score_mean.index:
      location_score = {
         'value': round(score_mean[index]*100, 2),
         'name': convert_city_to_stat(index),
      }
      data.append(location_score)
   return jsonify({'error_code':0,'data':data})

@app.route('/vaccine/sentiment_trend',methods = ['POST', 'GET'])
def vaccine_sentiment_trend():
   score_df = pd.read_csv('Result.csv')
   score_by_date = score_df.groupby(by = ['week'])
   score_mean = score_by_date.mean()['score_textblob']
   score_median = score_by_date.quantile(0.5)['score_textblob']
   score_quantile10 = score_by_date.quantile(0.1)['score_textblob']
   score_quantile90 = score_by_date.quantile(0.9)['score_textblob']
   data = []
   for index in score_mean.index:
      data_day = {
         'value': round(score_mean[index],4),
         'date': index,
         'range': [round(score_quantile10[index],4),round(score_quantile90[index],4)]
      }
      data.append(data_day)
   return jsonify({'error_code':0,'data':data})

# top 100 words related to vaccine
vaccine_words = ['covid19', 'covid', 'people', 'pfizer', 'australia', 'rollout', 'astrazeneca', 'us', 'doses', 'government', 'need', 'az', 'health', 'australians', 'first', 'new', 'risk', 'know', 'million', 'time', 'many', 'virus', 'think', 'good', 'cases', 'says', 'world', 'auspol', 'well', 'morrison', 'jab', 'work', 'coronavirus', 'year', 'deaths', 'quarantine', 'want', 'see', 'said', 'care', 'countries', 'news', 'workers', 'immunity', 'effective', 'scottmorrisonmp', '7news', 'mrna', 'flu', 'blood', 'week', 'clots', 'uk', 'enough', 'public', 'data', 'back', 'govt', 'months', 'next', 'last', 'right', 'program', 'everyone', 'safe', 'available', 'use', 'better', 'day', 'really', 'already', 'aged', 'end', 'moderna', 'federal', 'country', 'today', 'medical', 'long', 'population', 'greghuntmp', 'stop', 'states', 'pandemic', 'open', 'never', 'years', 'sure', 'point', 'days', 'minister', 'must', 'weeks', 'keep', 'roll', 'yes', 'wait', 'borders', 'due', 'india']
@app.route('/vaccine/words_cloud',methods = ['POST', 'GET'])
def vaccine_words_cloud():
   data = []
   wordcloud_vaccine_view_result = db.view('vaccine_related/Wordcloud_vaccine',group=True, keys=vaccine_words)
   word_count_vaccine = {}
   for r in wordcloud_vaccine_view_result :
      word_count_vaccine[r.key] = r.value
   # get top 80 results
   word_count_vaccine = sorted(word_count_vaccine.items(), key=lambda item:item[1], reverse=True)[:80]
   for item in word_count_vaccine:
      data.append({
         'text':  item[0],
         'value': item[1]
      })
   return {'error_code':0,'data':data}

@app.route('/vaccine/get_tweet_by_word',methods = ['POST', 'GET'])
def vaccine_get_tweet_by_word():
   if request.method == 'POST':
      word = json.loads(request.get_data(as_text=True))['word']
      contents = []
      for item in db.view('vaccine_related/Wordcloud_vaccine',include_docs=True,key=word, reduce=False,limit=100):
         contents.append(item.doc['full_text'])
      random_index = random.randint(0,len(contents) - 1)
      return jsonify({'error_code':0,'data':contents[random_index]})

@app.route('/vaccine/hashtag/words_cloud',methods = ['POST', 'GET'])
def vaccine_hashtag_words_cloud():
   data = []
   wordcloud_vaccine_view_result = db.view('vaccine_related/Wordcloud_hashtag_vaccine',group=True)
   word_count_vaccine = {}
   for r in wordcloud_vaccine_view_result :
      word_count_vaccine[r.key] = r.value
   word_count_vaccine = sorted(word_count_vaccine.items(), key=lambda item:item[1], reverse=True)[:50]
   for item in word_count_vaccine:
      data.append({
         'text': '#' + item[0],
         'value': item[1]
      })
   return {'error_code':0,'data':data}

@app.route('/vaccine/hashtag/get_tweet_by_word',methods = ['POST', 'GET'])
def vaccine_hashtag_get_tweet_by_word():
   if request.method == 'POST':
      word = json.loads(request.get_data(as_text=True))['word'][1:]
      contents = []
      for item in db.view('vaccine_related/Wordcloud_hashtag_vaccine',include_docs=True,key=word, reduce=False,limit=100):
         contents.append(item.doc['full_text'])
      random_index = random.randint(0,len(contents) - 1)
      return jsonify({'error_code':0,'data':contents[random_index]})

# top 100 words related to covid
covid_words = ['cases', 'vaccine', 'new', 'people', 'health', 'australia', 'deaths', 'us', 'pandemic', 'government', 'time', 'lockdown', 'nsw', 'need', 'test', 'victoria', 'virus', 'auspol', 'know', 'world', 'many', 'care', 'quarantine', 'risk', 'australian', 'first', 'work', 'live', 'masks', 'says', 'back', 'year', 'restrictions', 'day', 'good', 'news', 'covid19aus', 'state', 'today', 'see', 'help', 'hospital', 'positive', 'community', 'public', 'home', 'due', 'patients', 'well', 'response', 'spread', 'think', 'last', 'workers', 'outbreak', 'melbourne', '7news', 'hotel', 'days', 'sydney', 'support', 'much', 'india', 'million', 'say', 'crisis', 'tested', 'testing', 'great', 'covid19vic', 'vaccination', 'keep', 'right', 'covid19australia', 'travel', 'australians', 'aged', 'research', 'next', 'really', 'want', 'months', 'week', '2020', 'since', 'another', 'said', 'wa', 'long', 'china', 'uk', 'states', 'transmission', 'better', 'safe', 'every', 'country', 'social', 'open', 'use']
@app.route('/covid/words_cloud',methods = ['POST', 'GET'])
def covid_words_cloud():
   data = []
   wordcloud_covid_view_result = db.view('covid_related/Wordcloud_covid',group=True, keys=covid_words)
   word_count_covid = {}
   for r in wordcloud_covid_view_result :
      word_count_covid[r.key] = r.value
   # get top 80 results
   word_count_covid = sorted(word_count_covid.items(), key=lambda item:item[1], reverse=True)[:80]
   for item in word_count_covid:
      data.append({
         'text': item[0],
         'value': item[1]
      })
   return {'error_code':0,'data':data}

@app.route('/covid/get_tweet_by_word',methods = ['POST', 'GET'])
def covid_get_tweet_by_word():
   if request.method == 'POST':
      word = json.loads(request.get_data(as_text=True))['word']
      contents = []
      for item in db.view('covid_related/Wordcloud_covid',include_docs=True,key=word, reduce=False,limit=100):
         contents.append(item.doc['full_text'])
      random_index = random.randint(0,len(contents) - 1)
      return jsonify({'error_code':0,'data':contents[random_index]})

@app.route('/covid/hashtag/words_cloud',methods = ['POST', 'GET'])
def covid_hashtag_words_cloud():
   data = []
   wordcloud_covid_view_result = db.view('covid_related/Wordcloud_hashtag_covid',group=True)
   word_count_covid = {}
   for r in wordcloud_covid_view_result :
      if r.key not in ['covid19','covid','coronavirus','covid_19','covidー19']:
         word_count_covid[r.key] = r.value 
   word_count_covid = sorted(word_count_covid.items(), key=lambda item:item[1], reverse=True)[:60]
   for item in word_count_covid:
      data.append({
         'text': '#'+ item[0],
         'value': item[1]
      })
   return {'error_code':0,'data':data}

@app.route('/covid/hashtag/get_tweet_by_word',methods = ['POST', 'GET'])
def covid_hashtag_get_tweet_by_word():
   if request.method == 'POST':
      word = json.loads(request.get_data(as_text=True))['word'][1:]
      contents = []
      for item in db.view('covid_related/Wordcloud_hashtag_covid',include_docs=True,key=word, reduce=False,limit=100):
         contents.append(item.doc['full_text'])
      random_index = random.randint(0,len(contents) - 1)
      return jsonify({'error_code':0,'data':contents[random_index]})

if __name__ == '__main__':
   app.run(debug = True)