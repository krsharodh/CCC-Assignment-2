import couchdb
import json

user = "admin"
password = "admin"
couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))


######################################
####         General case         ####
######################################

# Count the total number of tweets in each city

map_fun_TweetCity = '''function (doc) { 
        emit(doc.uniform_location, 1);
    }
'''

reduce_fun_TweetCity = "_count"

db = couchserver["raw_tweets_from_timeline"]

#######################################
####   Scenario 1: covid related   ####
#######################################

# Count the number of tweets mentioned covid in each city in each year/month/day/hour

map_fun_CityDateTime = '''function (doc) {
    var text = doc.full_text.toLowerCase()
    if (text.indexOf('covid') != -1 || 
    text.indexOf('covid-19') != -1 ||
    text.indexOf('covid19') != -1)
        var date = new Date(doc.created_at); 
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDay() + 1;
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
        var month = date.getMonth() + 1;
        var day = date.getDay() + 1;
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
    if (text.indexOf('jobkeeper') != -1 || 
    text.indexOf('jobseeker') != -1 ||
    text.indexOf('job keeper') != -1 || 
    text.indexOf('job seeker') != -1)
        var date = new Date(doc.created_at); 
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDay() + 1;
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

######################################
####          AURIN Data          ####
######################################

map_fun_income = '''function (doc) {
        emit(doc.properties.lga_code_2016, doc.properties.median_tot_prsnl_inc_weekly)
    }
'''

data_income = {
        "_id": f"_design/income_doc",
        "views": {
            "income": {
                "map": map_fun_income
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
}

AURIN_db = couchserver["aurin_income"]
AURIN_db.save(data_income)

###########################################
#### Extra Data: Covid Confirmed Cases ####
###########################################

# sum the number of covid confirmed cases for each city

map_fun_CovidCases = '''function (doc) { 
        var date = new Date(doc.date); 
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDay() + 1;
        emit([doc.state_abbrev, year, month, day], parseInt(doc.confirmed));
    }
'''

reduce_fun_CovidCases = "_sum"

# Save Covid_cases related views to DB

Covid_db = couchserver["covid_cases"]

Cases_data = {
        "_id": f"_design/state_cases",
        "views": {
            "StateConfirmedCases_sum": {
                "map": map_fun_CovidCases,
                "reduce": reduce_fun_CovidCases
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
}

Covid_db.save(Cases_data)



################################
### Define Get View Function ###
################################

def get_view(db_name, doc_name, view_name, group_level = 0, reduce = 'false'):
    user = "admin"
    password = "admin"
    couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))
    db = couchserver[db_name]
    return db.view(name = doc_name + '/' + view_name, group_level = group_level, reduce = reduce)



###############################################
####             Data Analysis             ####
###############################################

######################################
####  Scenarion 1: covid related  ####
######################################

### 1. Proportion of covid tweets ###

# Create a list and each element in the list contained info about city name, number of tweets mentioned covid and total tweets
# e.g. Scenario_one_proportion = [{"city":{}, "metioned_covid":{}, "total_tweets": {}}]

Scenario_one_proportion = []

# Count the number of tweets mentioned covid in each city

covid_tweet_city = get_view(
    "raw_tweets_from_timeline", 
    "covid_related",
    "CityDateTime_count",
    1, 
    'true'
    )

for row in covid_tweet_city:
    Scenario_one_temp = {"city":{}, "metioned_covid":{}}
    Scenario_one_temp["city"] = row["key"][0]
    Scenario_one_temp["metioned_covid"] = row["value"]
    Scenario_one_proportion.append(Scenario_one_temp)
    print(row["key"], row["value"])

# Count the total number of tweets in each city

tweet_city = get_view(
    "raw_tweets_from_timeline", 
    "covid_related",
    "Tweet_count", 
    1, 
    'true'
    )

for row in tweet_city:
    print(row["key"], row["value"])
    for i in range(len(Scenario_one_proportion)):
        if row["key"] == Scenario_one_proportion[i]["city"]:
            Scenario_one_proportion[i]["total_tweets"] = row["value"]


### 2. correlation between covid tweets and confirmed cases ###

# Create a list for each city and each element/dictionary in the list contains three variables
# e.g. city_list = [{"time":{}, "tweets": {}, "cases": {}}]

# Create a series of empty list for each city

Scenario_two_adelaide = []
Scenario_two_brisbane = []
Scenario_two_canberra = []
Scenario_two_darwin = []
Scenario_two_hobart = []
Scenario_two_melbourne = []
Scenario_two_perth = []
Scenario_two_sydney = []


covid_cases_statedate = get_view(
    "covid_cases", 
    "state_cases", 
    "StateConfirmedCases_sum", 
    4, 
    'true'
    )


covid_tweet_citymonth = get_view(
    "raw_tweets_from_timeline", 
    "covid_related",
    "CityDateTime_count", 
    4, 
    'true'
    )


def add_case(scenario_list, datetime, cases):
    Scenario_two_temp = {"time":{}, "cases": {}}
    Scenario_two_temp["time"] = datetime
    Scenario_two_temp["cases"] = cases
    return scenario_list.append(Scenario_two_temp)

for row in covid_cases_statedate:
    Datetime = [row["key"][1], row["key"][2], row["key"][3]]
    Date_time = "-".join(str(e).zfill(2) for e in Datetime)
    if(row["key"][0] == 'ACT'):
        add_case(Scenario_two_canberra , Date_time, row["value"])
    elif (row["key"][0] == 'NSW'):
        add_case(Scenario_two_sydney , Date_time, row["value"])
    elif (row["key"][0] == 'NT'):
        add_case(Scenario_two_darwin , Date_time, row["value"])
    elif (row["key"][0] == 'QLD'):
        add_case(Scenario_two_brisbane , Date_time, row["value"])
    elif (row["key"][0] == 'SA'):
        add_case(Scenario_two_adelaide , Date_time, row["value"])
    elif (row["key"][0] == 'TAS'):
        add_case(Scenario_two_hobart , Date_time, row["value"])
    elif (row["key"][0] == 'VIC'):
        add_case(Scenario_two_melbourne , Date_time, row["value"])
    elif (row["key"][0] == 'WA'):
        add_case(Scenario_two_perth , Date_time, row["value"])

def add_tweets(scenario_list):
    for i in range(len(scenario_list)):
        for row in covid_tweet_citymonth:
            Datetime = [row["key"][1], row["key"][2], row["key"][3]]
            Date_time = "-".join(str(e).zfill(2) for e in Datetime)
            if scenario_list[i]["time"] == Date_time:
                scenario_list[i]["tweets"] = row["value"]
            else:
                scenario_list[i]["tweets"] = 0

add_tweets(Scenario_two_canberra)
add_tweets(Scenario_two_sydney)
add_tweets(Scenario_two_darwin)
add_tweets(Scenario_two_brisbane)
add_tweets(Scenario_two_adelaide)
add_tweets(Scenario_two_hobart)
add_tweets(Scenario_two_melbourne)
add_tweets(Scenario_two_perth)


######################################
#### Scenarion 2: vaccine related ####
######################################

### 1. Proportion of vaccine tweets ###

# Create a list and each element in the list contained info about city name, number of tweets mentioned vaccine, total tweets
# e.g. Scenario_two_proportion = [{"city":{}, "metioned_vaccine":{}, "total_tweets": {}}]

Scenario_two_proportion = []

# Count the number of tweets mentioned vaccine in each city

vaccine_tweet_city = get_view(
    "raw_tweets_from_timeline", 
    "vaccine_related",
    "Vaccine_CityDateTime_count", 
    1, 
    'true'
    )

for row in vaccine_tweet_city:
    Scenario_two_temp = {"city":{}, "metioned_vaccine":{}}
    Scenario_two_temp["city"] = row["key"][0]
    Scenario_two_temp["metioned_vaccine"] = row["value"]
    Scenario_two_proportion.append(Scenario_two_temp)

# Count the total number of tweets in each city

tweet_city = get_view(
    "raw_tweets_from_timeline", 
    "covid_related",
    "Tweet_count", 
    1, 
    'true'
    )

for row in tweet_city:
    for i in range(len(Scenario_two_proportion)):
        if row["key"] == Scenario_two_proportion[i]["city"]:
            Scenario_two_proportion[i]["total_tweets"] = row["value"]



######################################
####   Scenarion 3: job related   ####
######################################

def get_proportion_tweets(scenario_list, job_tweet_city, tweet_city):

    # Count the number of tweets mentioned jobkeeper/jobseeker in each city

    for row in job_tweet_city:
        Scenario_temp = {"city":{}, "metioned_jobkeeper":{}}
        scenario_list["city"] = row["key"][0]
        scenario_list["metioned_jobkeeper"] = row["value"]
        scenario_list.append(Scenario_temp)
    
    # Count the total number of tweets in each city

    for row in tweet_city:
        for i in range(len(scenario_list)):
            if row["key"] == scenario_list[i]["city"]:
                scenario_list[i]["total_tweets"] = row["value"]
    
    return scenario_list

def get_aurin_info(scenario_list, aurin_info, info_name):
    for row in aurin_info:
        for i in range(len(scenario_list)):
            if(row['key'] == '40070' and scenario_list[i]["city"] == 'adelaide'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '31000' and scenario_list[i]["city"] == 'brisbane'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '89399' and scenario_list[i]["city"] == 'canberra'):
                scenario_list[i][info_name] = row['value']           
            elif(row['key'] == '71000' and scenario_list[i]["city"] == 'darwin'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '62810' and scenario_list[i]["city"] == 'hobart'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '24600' and scenario_list[i]["city"] == 'melbourne'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '57080' and scenario_list[i]["city"] == 'perth'):
                scenario_list[i][info_name] = row['value']
            elif(row['key'] == '17200' and scenario_list[i]["city"] == 'sydney'):
                scenario_list[i][info_name] = row['value']
    
    return scenario_list


### 1. Proportion of jobkeeper/jobseeker tweets vs median_weekly_personal_income ###

# Create a list and each element in the list contained info about city name, number of tweets mentioned job^ and income
# e.g. Scenario_three = [{"city":{}, "metioned_jobkeeper":{},, "total_tweets": {}, "median_weekly_personal_income": {}}]

Scenario_three_proportion = []

# Count the number of tweets mentioned jobkeeper/jobseeker in each city

job_tweet_city = get_view(
    "raw_tweets_from_timeline", 
    "job_related",
    "Job_CityDateTime_count", 
    1, 
    'true'
)

Scenario_three_proportion = get_proportion_tweets(Scenario_three_proportion, job_tweet_city, tweet_city)

# add median weekly personal income information to each city

income_info = get_view(
    "aurin_income", 
    "income_doc", 
    "income"
)

Scenario_three_proportion = get_aurin_info(Scenario_three_proportion, income_info, 'median_weekly_personal_income')


### 2. Proportion of jobkeeper/jobseeker tweets vs jobkeeper payment ###

Scenario_three_payment = []

Scenario_three_payment = get_proportion_tweets(Scenario_three_payment, job_tweet_city, tweet_city)

jobseeker_payment_info = get_view(
    "aurin_quarterly_payment", 
    "JobseekerPayment_doc", 
    "quarterly_payment"
)

Scenario_three_payment = get_aurin_info(Scenario_three_payment, jobseeker_payment_info, 'jobseeker_payment')


### 3. Proportion of jobkeeper/jobseeker tweets vs aged between 15 and 64 ###

Scenario_three_aged = []

Scenario_three_aged = get_proportion_tweets(Scenario_three_aged, job_tweet_city, tweet_city)

aged_info = get_view(
    "aurin_regional_population", 
    "Aged_15_64_doc", 
    "Aged_15_64"
)

Scenario_three_aged = get_aurin_info(Scenario_three_aged, aged_info, 'Aged_15_64_percentage')
