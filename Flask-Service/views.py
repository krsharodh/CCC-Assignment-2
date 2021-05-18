import requests
from requests.api import get
import couchdb
import json

user = "admin"
password = "admin"
couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))

db = couchserver["raw_tweets_from_timeline"]

######################################
#### General case ####
######################################

# Count the total number of tweets in each city

map_fun_TweetCity = '''function (doc) { 
        emit(doc.uniform_location, 1);
    }
'''

reduce_fun_TweetCity = "_count"

######################################
#### Scenarion 1: covid related ####
######################################

# Count the number of tweets mentioned covid in each city in each year/month/day/hour

map_fun_CityDateTime = '''function (doc) {
    var text = doc.full_text.toLowerCase()
    if (text.indexOf('covid') != -1 || 
    text.indexOf('covid-19') != -1 ||
    text.indexOf('covid19') != -1)
        var date = new Date(doc.created_at); 
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDay();
        var hour = date.getHours();
        var location = doc.uniform_location
        emit([location, year, month, day, hour], 1)
    }
'''

reduce_fun_CityDateTime = "_count"

data_covid = {
        "_id": f"_design/covid_related",
        "views": {
            "Tweet_count": {
                "map": map_fun_TweetCity,
                "reduce": reduce_fun_TweetCity
            },
            "CityDateTime_count": {
                "map": map_fun_CityDateTime,
                "reduce": reduce_fun_CityDateTime
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
}

db.save(data_covid)

######################################
#### Scenarion 2: vaccine related ####
######################################

# Count the number of tweets mentioned vaccine in each city in each year/month/day/hour

map_fun_Vaccine_CityDateTime = '''function (doc) {
    var text = doc.full_text.toLowerCase()
    if (text.indexOf('vaccine') != -1 ||
     text.indexOf('vaccinate') != -1 ||
     text.indexOf('vaccination') != -1)
        var date = new Date(doc.created_at); 
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDay();
        var hour = date.getHours();
        var location = doc.uniform_location
        emit([location, year, month, day, hour], 1)
    }
'''

reduce_fun_Vaccine_CityDateTime = "_count"

data_vaccine = {
        "_id": f"_design/vaccine_related",
        "views": {
            "Vaccine_CityDateTime_count": {
                "map": map_fun_Vaccine_CityDateTime,
                "reduce": reduce_fun_Vaccine_CityDateTime
            },
            
        },
        "language": "javascript",
        "options": {"partitioned": False}
}

db.save(data_vaccine)

######################################
####   Scenarion 3: job related   ####
######################################

# Count the number of tweets mentioned jobseeker or jobkeeper in each city in each year/month/day/hour

map_fun_job_CityDateTime = '''function (doc) {
    var text = doc.full_text.toLowerCase()
    if (doc.full_text.indexOf('jobkeeper') != -1 || doc.full_text.indexOf('jobseeker') != -1)
        var date = new Date(doc.created_at); 
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDay();
        var hour = date.getHours();
        var location = doc.uniform_location
        emit([location, year, month, day, hour], 1)
    }
'''

reduce_fun_job_CityDateTime = "_count"

data_job = {
        "_id": f"_design/job_related",
        "views": {
            "Job_CityDateTime_count": {
                "map": map_fun_job_CityDateTime,
                "reduce": reduce_fun_job_CityDateTime
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
}

db.save(data_job)

### Define Get View Function ###

def get_view(db_name, doc_name, view_name, group_level):

    return requests.get(f"http://{user}:{password}@172.26.133.161:5984/{db_name}/_design/{doc_name}/_view/{view_name}?reduce=true&group_level={group_level}")



######################################
#### Scenarion 1: covid related ####
######################################

# Count the number of tweets mentioned covid in each city
covid_tweet_city = json.loads(get_view("raw_tweets_from_timeline", "covid_related","CityDateTime_count", 1).content.decode("utf-8"))
for row in covid_tweet_city['rows']:
    print(row["key"], row["value"])

# Count the total number of tweets in each city

tweet_city = json.loads(get_view("raw_tweets_from_timeline", "covid_related","Tweet_count", 1).content.decode("utf-8"))
for row in tweet_city['rows']:
    print(row["key"], row["value"])

Scenario_one = []

# Count the number of tweets mentioned covid in each city
covid_tweet_city = json.loads(get_view("raw_tweets_from_timeline", "covid_related","CityDateTime_count", 1).content.decode("utf-8"))
for row in covid_tweet_city['rows']:
    Scenario_one_temp = {"city":{}, "metioned_covid":{}}
    Scenario_one_temp["city"] = row["key"][0]
    Scenario_one_temp["metioned_covid"] = row["value"]
    Scenario_one.append(Scenario_one_temp)
    print(row["key"], row["value"])

# Count the total number of tweets in each city

tweet_city = json.loads(get_view("raw_tweets_from_timeline", "covid_related","Tweet_count", 1).content.decode("utf-8"))
for row in tweet_city['rows']:
    print(row["key"], row["value"])
    for i in range(len(Scenario_one)):
        if row["key"] == Scenario_one[i]["city"]:
            Scenario_one[i]["total_tweets"] = row["value"]


######################################
#### Scenarion 2: vaccine related ####
######################################

# Count the number of tweets mentioning COVID in each city each month

covid_tweet_citymonth = json.loads(get_view("raw_tweets_from_timeline", "covid_related","CityDateTime_count", 3).content.decode("utf-8"))
for row in covid_tweet_citymonth['rows']:
    print(row["key"], row["value"])


######################################
####   Scenarion 3: job related   ####
######################################

# Count the number of tweets mentioned jobkeeper/jobseeker in each city
Job_CityDateTime = json.loads(get_view("raw_tweets_from_timeline", "job_related","Job_CityDateTime_count", 1).content.decode("utf-8"))
for row in Job_CityDateTime['rows']:
    print(row["key"], row["value"])