from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import *
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route('/sentiment_score',methods = ['POST', 'GET'])
def sentiment_score():
   data = [{'name':'New South Wales','value':2030},
   {'name':'Queensland','value':2000},
   {'name':'South Australia','value': 1500},
   {'name':'Western Australia','value': 1200},
   {'name':'Victoria','value': 115},
   {'name':'Northern Territory','value':50},
   {'name':'Australian Capital Territory','value':400}]
   return jsonify({'error_code':0,'data':data})

@app.route('/sentiment_trend',methods = ['POST', 'GET'])
def sentiment_trend():
   score_df = pd.read_csv('Result.csv')
   score_by_date = score_df.groupby(by = ['week'])
   score_mean = score_by_date.mean()['score_textblob']
   score_median = score_by_date.quantile(0.5)['score_textblob']
   score_quantile10 = score_by_date.quantile(0.1)['score_textblob']
   score_quantile90 = score_by_date.quantile(0.9)['score_textblob']
   data = []
   for index in score_mean.index:
      data_day = {
         'value': score_mean[index],
         'date': index,
         'l': score_quantile10[index],
         'u': score_quantile90[index]
      }
      data.append(data_day)
   return jsonify({'error_code':0,'data':data})

@app.route('/words_cloud',methods = ['POST', 'GET'])
def words_cloud():
   data = [{'text': 'covid19', 'value': 1814}, {'text': 'covid', 'value': 1657}, {'text': 'people', 'value': 1476}, {'text': 'pfizer', 'value': 1398}, {'text': 'australia', 'value': 1117}, {'text': 'dose', 'value': 908}, {'text': 'astrazeneca', 'value': 897}, {'text': 'us', 'value': 794}, {'text': 'million', 'value': 781}, {'text': 'rollout', 'value': 698}, {'text': 'new', 'value': 641}, {'text': 'health', 'value': 630}, {'text': 'risk', 'value': 626}, {'text': 'year', 'value': 614}, {'text': 'az', 'value': 608}, {'text': 'case', 'value': 540}, {'text': 'good', 'value': 532}, {'text': 'first', 'value': 517}, {'text': 'government', 'value': 494}, {'text': 'death', 'value': 489}, {'text': 'news', 'value': 483}, {'text': 'virus', 'value': 481}, {'text': 'give', 'value': 477}, {'text': 'world', 'value': 476}, {'text': 'countries', 'value': 465}, {'text': 'time', 'value': 454}, {'text': 'variant', 'value': 449}, {'text': '7news', 'value': 430}, {'text': 'uk', 'value': 430}, {'text': 'work', 'value': 425}, {'text': 'auspol', 'value': 418}, {'text': 'week', 'value': 415}, {'text': 'well', 'value': 407}, {'text': 'effective', 'value': 401}, {'text': 'coronavirus', 'value': 392}, {'text': 'immunity', 'value': 372}, {'text': 'trial', 'value': 364}, {'text': 'efficacy', 'value': 360}, {'text': 'cases', 'value': 352}, {'text': 'dose', 'value': 350}, {'text': 'going', 'value': 348}, {'text': 'want', 'value': 348}, {'text': 'work', 'value': 331}, {'text': 'much', 'value': 325}, {'text': 'data', 'value': 320}, {'text': 'mrna', 'value': 319}, {'text': 'see', 'value': 312}, {'text': 'use', 'value': 311}, {'text': 'better', 'value': 304}, {'text': 'population', 'value': 303}, {'text': 'got', 'value': 302}, {'text': 'blood', 'value': 301}, {'text': 'stop', 'value': 298}, {'text': 'safe', 'value': 293}, {'text': 'go', 'value': 284}, {'text': 'say', 'value': 278}, {'text': 'deaths', 'value': 277}, {'text': 'flu', 'value': 275}, {'text': 'yet', 'value': 275}, {'text': 'already', 'value': 274}, {'text': 'says', 'value': 270}, {'text': 'everyone', 'value': 269}, {'text': 'public', 'value': 265}, {'text': 'country', 'value': 264}, {'text': 'right', 'value': 264}, {'text': 'jab', 'value': 263}, {'text': 'australian', 'value': 262}, {'text': 'way', 'value': 262}, {'text': 'australians', 'value': 260}, {'text': 'end', 'value': 260}, {'text': 'said', 'value': 259}, {'text': 'back', 'value': 252}, {'text': 'years', 'value': 251}, {'text': 'long', 'value': 247}, {'text': 'next', 'value': 246}, {'text': 'morrison', 'value': 242}, {'text': 'herd', 'value': 241}, {'text': 'administered', 'value': 240}, {'text': 'quarantine', 'value': 234}, {'text': 'care', 'value': 230}, {'text': 'india', 'value': 228}, {'text': 'infection', 'value': 227}]
   return jsonify({'error_code':0,'data':data})


if __name__ == '__main__':
   app.run(debug = True)