import pandas as pd
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from json_functions_v2 import *
from pitch_functions import *
import warnings
uri = "mongodb+srv://xxxxxx:yyyyyy@mongoplayers.xp8lika.mongodb.net/?retryWrites=true&w=majority&appName=MongoPlayers"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['xG']
collection = db['shots']
warnings.simplefilter(('ignore'))

def collect_existing_games():
    collection = db['shots']
    unique_matches = collection.distinct('match')
    print(len(unique_matches))
    return unique_matches

def check_unique_matches(match: int, unique_matches:list, unmatched:list, root:str):

    if match not in unique_matches:
        unmatched.append(match)
        print(root)

    return unmatched

unique_matches = collect_existing_games()
root_dir = '../GameData'
temp_df = pd.DataFrame()
print(f'Pre update record count : {collection.count_documents({})}')


for root, dirs, files in os.walk(root_dir):
    print(f'{root}')
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('.html'):
            if int(file.split(".")[0]) not in unique_matches:
                path_parts = root.split(os.sep)
                # Ensure the path_parts list has enough elements to unpack
                if len(path_parts) >= 4:
                    country, league, year = path_parts[-3:]
                    # Append the information to the data list
                    match_html_path = f'{root}/{str(file)}'
                    try:
                        json_data_txt = extract_json_from_html(match_html_path)  # get data from match file
                        data = json.loads(json_data_txt)  # store text for processing
                        (events_dict, players_df, players_dict, teams_dict, home_team,
                         away_team) = extract_data_from_dict(data)  # call function to read the json info into a
                        # series of dictionaries and dataframes.  We are only interested in the events_dict
                        events_df, df = get_events_df(events_dict)  # call get_events functionon the events_dict
                        # to get the dataframe, df, with all events
                        shots_df = df[df['isShot'] == True]  # filtered dataframe to include only shots
                        shots_df['dist'] = ""  # create new field for 'dist' distance from goal
                        shots_df['angle'] = ""  # create new field for 'angle' from goal
                        shots_df['zone'] = ""  # create new field for 'zone' on pitch

                        shots_df['country'] = country  # field to store the country
                        shots_df['league'] = league  # field to store the league
                        shots_df['year'] = year  # field to store the year
                        shots_df['match'] = file.split(".")[0]  # field to store match no

                        for index, row in shots_df.iterrows():
                            dist = get_shot_distance(row['x'],
                                                     row['y'])  # using co-ordinates call function to calculate distance
                            angle = get_shot_angle(row['x'],
                                                   row['y'])  # using co-ordinates call function to calculate angle
                            zone = get_pass_shot_zones(row['x'],
                                                       row['y'])  # using co-ordinates call function to calculate zone

                            shots_df['dist'].at[index] = dist  # store distance
                            shots_df['angle'].at[index] = angle  # store angle
                            shots_df['zone'].at[index] = zone  # store zone
                        temp_df = pd.concat(
                            [temp_df, shots_df])  # combine shots_df from this match with the current temp_df
                        output_folder = f'{root_dir}'
                        output_file = f'{output_folder}/game_temp.csv'
                        temp_df.to_csv(output_file)  # save temp file as we go along
                        print(f'{country} : {league} : {year} : {file} complete')
                    except:
                        pass
# shot_df = temp_df[['x', 'isGoal', 'isShot', 'prevEventType', 'angle', 'bodyPart', 'assisted', 'shotBlocked', 'shotOnTarget', 'shotOffTarget',
#                   'penalty', 'bigChance', 'cumulative_seconds', 'dist', 'zone', 'country', 'league', 'year', 'match']]
shot_df = temp_df[['x', 'isGoal', 'isShot', 'prevEventType', 'angle', 'bodyPart', 'assisted', 'shotBlocked', 'shotOnTarget', 'shotOffTarget',
                   'penalty', 'bigChance', 'cumulative_seconds', 'dist', 'country', 'league', 'year', 'match']]

data_to_upload = shot_df.to_dict('records')

try:
    collection.insert_many(data_to_upload)
    print(f'Records inserted successfully')

except:
    raise
    print(f"Insert failed at index {index}")

print(f'Post update record count : {collection.count_documents({})}')

