import csv
import json

with open('COVID_AU_state_daily_change.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open('COVID_AU_state_daily_change.json', 'w') as f:
    json.dump(rows, f)