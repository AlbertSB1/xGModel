import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://xxxxxx:yyyyyy@mongoplayers.xp8lika.mongodb.net/?retryWrites=true&w=majority&appName=MongoPlayers"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['xG']
collection = db['shots']


# Send a ping to confirm a successful connection
def pingMongo():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def insertShots(shot_file):

    df = pd.read_csv(shot_file)
    shot_df = df[['x', 'isGoal', 'isShot', 'prevEventType', 'angle', 'bodyPart', 'assisted', 'shotBlocked', 'shotOnTarget', 'shotOffTarget',
                  'penalty', 'bigChance', 'cumulative_seconds', 'dist', 'zone', 'country', 'league', 'year', 'match']]

    data_to_upload = shot_df.to_dict('records')
    try:
        collection.insert_many(data_to_upload)
        print("Collection inserted successfully")
    except:
        print("Insert failed")

def examineShotFile(shot_file):
    df = pd.read_csv(shot_file)
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    print(f'Number of rows: {num_rows}')
    print(f'Number of columns: {num_cols}')

    shots = df[df['isShot'] == True].shape[0]
    goals = df[df['isGoal'] == True].shape[0]

    print(f'Shots : {shots}, Goals : {goals}')

    duplicates = df.duplicated().any()

    # Check if there are any duplicates
    if duplicates:
        print("There are duplicate rows in the DataFrame.")
    else:
        print("There are no duplicate rows in the DataFrame.")

def retrieveShots(collection):
    projection = {
        'isGoal': 1,
        'isShot': 1,
        'prevEventType': 1,
        'angle': 1,
        'bodyPart': 1,
        'x': 1,
        'match':1,
        'country':1,
        'league':1,
        'year':1,
        '_id': 0
    }

    query = {'league':{'$ne':'WSL'}}

    match_records = list(collection.find(query, projection))
    print(len(match_records))
    df = pd.DataFrame(match_records)
    unique_matches = df['match'].nunique()
    print(f'Number of unique values in "match" field: {unique_matches}')
    print(f'Number of rows in {collection.name} : {len(match_records)}')

pingMongo()
