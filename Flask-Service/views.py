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
        var day = date.getDate();
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
        var day = date.getDate();
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
        var day = date.getDate();
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
        var day = date.getDate();
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
