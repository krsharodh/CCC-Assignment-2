import requests
import couchdb
import json


try :
    requests.put('http://admin:admin@172.26.133.161:5984/covid_cases?q=2&n=4')
    requests.put('http://admin:admin@172.26.133.161:5984/aurin_income?q=2&n=4')
    requests.put('http://admin:admin@172.26.133.161:5984/aurin_regional_population?q=2&n=4')
    requests.put('http://admin:admin@172.26.133.161:5984/aurin_quarterly_payment?q=2&n=4')
except:
    pass

user = "admin"
password = "admin"
couchserver = couchdb.Server("http://%s:%s@172.26.133.161:5984/" % (user, password))

covid_db = couchserver["covid_cases"]
aurin_income_db = couchserver["aurin_income"]
aurin_regional_population_db = couchserver["aurin_regional_population"]
aurin_quarterly_payment_db = couchserver["aurin_quarterly_payment"]

with open('data2357255522807394857.json') as jsonfile:
    rows = json.load(jsonfile)['features']
    for db_entry in rows:
        aurin_income_db.save(db_entry)

with open('ABS_-_Regional_Population_-_Summary_Statistics__LGA__2018.json') as jsonfile:
    rows = json.load(jsonfile)['features']
    for db_entry in rows:
        aurin_regional_population_db.save(db_entry)

with open('DSS_-_Quarterly_Payment_Recipients__LGA__June_2020.json') as jsonfile:
    rows = json.load(jsonfile)['features']
    for db_entry in rows:
        aurin_quarterly_payment_db.save(db_entry)

with open('COVID_AU_state_daily_change.json') as jsonfile:
    rows = json.load(jsonfile)
    for db_entry in rows:
        covid_db.save(db_entry)

