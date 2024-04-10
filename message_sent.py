
import pandas as pd
import os 
from pymongo import MongoClient
import json
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client['market_place_scraped_data']
collection = db['post_data']

df = pd.read_csv(os.path.join(os.getcwd(),'src','post_data.csv'))
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

json_data = df.to_json(orient='records')

new_record = []
for record in json.loads(json_data):
    link = record['link']
    existing_record = collection.find_one({'link': link})

    if existing_record:
        record['upgrade_date'] = current_date
        record.pop('upload_date', None)
        collection.update_one({'link': link}, {'$set': record})
    else:
        profile_link = record['profile_link']
        existing_profile_record = list(collection.find({'profile_link': profile_link}).sort('message_date', -1).limit(1))
        
        if len(existing_profile_record) > 0:
            latest_profile_record = existing_profile_record[0]
            message_date = latest_profile_record.get('message_date')

            if message_date:
                date_diff = datetime.now() - datetime.strptime(message_date, '%Y-%m-%d %H:%M:%S')
                 
                if date_diff.days >= 20:
                    record['message_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record['message_status'] = 'yes'
                    collection.insert_one(record)
                    print('Send a message 1')
                    new_record.append(record)
                elif date_diff.days < 20 and latest_profile_record.get('message_status', 'no') == 'no':
                    record['message_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record['message_status'] = 'yes'
                    collection.insert_one(record)
                    print('Send a message 2')
                    new_record.append(record)
                elif date_diff.days < 20 and latest_profile_record.get('message_status', 'no') == 'yes':
                    record['message_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    record['message_status'] = 'no'
                    collection.insert_one(record)
                    print('does not Send a message')
        else:
            record['message_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record['message_status'] = 'yes'
            collection.insert_one(record)
            print('Send a message 3')
            new_record.append(record)

client.close()
# print(len(new_record))
# print(new_record['profile_link','profile_name'])

for record in new_record:
    record['messsage']='Hi '+record['profile_name']+ ' Im Avishka Gimhana Ignore this message.'

message_data=[]
for record in new_record:
    message_data.append([record['profile_link'],record['messsage']])

