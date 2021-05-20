import couchdb
import json
import csv
import pandas as pd

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
    text.indexOf('vaccinat') != -1 || 
    text.indexOf('pfizer') != -1 || 
    text.indexOf('astrazeneca') != -1)
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
    if (text.indexOf('jobkeeper') != -1 || text.indexOf('jobseeker') != -1 ||
    text.indexOf('job keeper') != -1 || text.indexOf('job seeker') != -1)
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
    user = "admin"
    password = "admin"
    couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))
    db = couchserver[db_name]
    return db.view(name = doc_name + '/' + view_name, group_level = group_level, reduce='true')



######################################
####  Scenarion 1: covid related  ####
######################################

### 1. Proportion of covid tweets ###

# Create a list and each element in the list contained info about city name, number of tweets mentioned covid and total tweets
# e.g. Scenario_one_proportion = [{"city":{}, "metioned_covid":{}, "total_tweets": {}}]

Scenario_one_proportion = []

# Count the number of tweets mentioned covid in each city
covid_tweet_city = get_view("raw_tweets_from_timeline", "covid_related","CityDateTime_count", 1)
for row in covid_tweet_city['rows']:
    Scenario_one_temp = {"city":{}, "metioned_covid":{}}
    Scenario_one_temp["city"] = row["key"][0]
    Scenario_one_temp["metioned_covid"] = row["value"]
    Scenario_one_proportion.append(Scenario_one_temp)
    print(row["key"], row["value"])

# Count the total number of tweets in each city

tweet_city = get_view("raw_tweets_from_timeline", "covid_related","Tweet_count", 1)
for row in tweet_city['rows']:
    print(row["key"], row["value"])
    for i in range(len(Scenario_one_proportion)):
        if row["key"] == Scenario_one_proportion[i]["city"]:
            Scenario_one_proportion[i]["total_tweets"] = row["value"]


### 2. correlation between covid tweets and confirmed cases ###

# Create a list for each city and each element/dictionary in the list contains three variables
# e.g. city_list = [{"time":{}, "tweets": {}, "cases": {}}]

# Function for adding the number of tweets mentioned covid in particular city and time to the city list

def add_value(scenario_list, key, value):
    Scenario_two_temp = {"time":{}, "tweets": {}}
    Datetime = [key[1], key[2] + 1, key[3] + 1]
    Scenario_two_temp["time"] = "-".join(str(e).zfill(2) for e in Datetime)

    Scenario_two_temp["tweets"] = value
    return scenario_list.append(Scenario_two_temp)

#  Function for adding the confirmed cases in each state in particular time to the city list

def add_case(scenario_list, case_list):
    for i in range(len(scenario_list)):
        if scenario_list[i]["time"] in set(case_ACT.date):
            index = case_list[case_list['date'] == scenario_list[i]["time"]].index.values[0]
            scenario_list[i]["cases"] = case_list.at[index,'confirmed']

# Create a series of empty list for each city

Scenario_one_adelaide = []
Scenario_one_brisbane = []
Scenario_one_canberra = []
Scenario_one_darwin = []
Scenario_one_hobart = []
Scenario_one_melbourne = []
Scenario_one_perth = []
Scenario_one_sydney = []

# Read the number of tweets mentioned covid group/aggregated by location, year, month, date

covid_tweet_citymonth = get_view("raw_tweets_from_timeline", "covid_related","CityDateTime_count", 4)

# Add the number of tweets mentioned covid and date to each city list 

for row in covid_tweet_citymonth['rows']:
    if "adelaide" == row["key"][0]:
        add_value(Scenario_one_adelaide, row["key"], row["value"])
    elif "brisbane" == row["key"][0]:
        add_value(Scenario_one_brisbane, row["key"], row["value"])
    elif "canberra" == row["key"][0]:
        add_value(Scenario_one_canberra, row["key"], row["value"])
    elif "darwin" == row["key"][0]:
        add_value(Scenario_one_darwin, row["key"], row["value"])
    elif "hobart" == row["key"][0]:
        add_value(Scenario_one_hobart, row["key"], row["value"])
    elif "melbourne" == row["key"][0]:
        add_value(Scenario_one_melbourne, row["key"], row["value"])
    elif "perth" == row["key"][0]:
        add_value(Scenario_one_perth, row["key"], row["value"])
    elif "sydney" == row["key"][0]:
        add_value(Scenario_one_sydney, row["key"], row["value"])

# Read the covid cases dataset

with open('COVID_AU_state_daily_change.csv', newline='') as f:
    reader = csv.reader(f) 
    case = pd.DataFrame(reader) 
    new_header = case.iloc[0] 
    case = case[1:]
    case.columns = new_header 

    # Create a series of lists to store the confirmed cases information for each state

    case_ACT = case.loc[case['state_abbrev'] == 'ACT']
    case_NSW = case.loc[case['state_abbrev'] == 'NSW']
    case_NT = case.loc[case['state_abbrev'] == 'NT']
    case_QLD = case.loc[case['state_abbrev'] == 'QLD']
    case_SA = case.loc[case['state_abbrev'] == 'SA']
    case_TAS = case.loc[case['state_abbrev'] == 'TAS']
    case_VIC = case.loc[case['state_abbrev'] == 'VIC']
    case_WA = case.loc[case['state_abbrev'] == 'WA']

# Add the confirmed cases info to each city list

add_case(Scenario_one_adelaide, case_SA)
add_case(Scenario_one_brisbane, case_QLD)
add_case(Scenario_one_canberra, case_ACT)
add_case(Scenario_one_darwin, case_NT)
add_case(Scenario_one_hobart, case_TAS)
add_case(Scenario_one_melbourne, case_VIC)
add_case(Scenario_one_perth, case_WA)
add_case(Scenario_one_sydney, case_NSW)


######################################
#### Scenarion 2: vaccine related ####
######################################

### 1. Proportion of vaccine tweets ###

# Create a list and each element in the list contained info about city name, number of tweets mentioned covid vaccine, total tweets
# e.g. Scenario_two_proportion = [{"city":{}, "metioned_vaccine":{}, "total_tweets": {}}]

Scenario_two_proportion = []

# Count the number of tweets mentioned covid in each city
vaccine_tweet_city = get_view("raw_tweets_from_timeline", "vaccine_related","Vaccine_CityDateTime_count", 1)
for row in vaccine_tweet_city['rows']:
    Scenario_two_temp = {"city":{}, "metioned_vaccine":{}}
    Scenario_two_temp["city"] = row["key"][0]
    Scenario_two_temp["metioned_vaccine"] = row["value"]
    Scenario_two_proportion.append(Scenario_two_temp)

# Count the total number of tweets in each city

tweet_city = get_view("raw_tweets_from_timeline", "covid_related","Tweet_count", 1)
for row in tweet_city['rows']:
    for i in range(len(Scenario_two_proportion)):
        if row["key"] == Scenario_two_proportion[i]["city"]:
            Scenario_two_proportion[i]["total_tweets"] = row["value"]

######################################
####   Scenarion 3: job related   ####
######################################

# Count the number of tweets mentioned jobkeeper/jobseeker in each city
Job_CityDateTime = get_view("raw_tweets_from_timeline", "job_related","Job_CityDateTime_count", 1)
for row in Job_CityDateTime['rows']:
    print(row["key"], row["value"])