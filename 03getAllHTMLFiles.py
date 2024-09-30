import os
import pandas as pd
from json_functions_v2 import *
from pitch_functions import *
import warnings

# Define the root directory
root_dir = '../GameData'

# Prepare a list to store the data
data = []
count = 0
temp_df = pd.DataFrame()
warnings.simplefilter('ignore')
prev_country = ''
prev_league = ''

# Walk through the directory
for root, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('.html'):
            # Split the path to extract country, league, and year
            path_parts = root.split(os.sep)
            # Ensure the path_parts list has enough elements to unpack
            if len(path_parts) >= 4:
                country, league, year = path_parts[-3:]
                # Append the information to the data list
                match_html_path = f'{root}/{str(file)}'
                if country == prev_country and league == prev_league:
                    pass
                else:
                    temp_df = pd.DataFrame()
                try:
                    json_data_txt = extract_json_from_html(match_html_path) #get data from match file
                    data = json.loads(json_data_txt) #store text for processing
                    (events_dict, players_df, players_dict, teams_dict, home_team,
                            away_team) = extract_data_from_dict(data) #call function to read the json info into a
                            # series of dictionaries and dataframes.  We are only interested in the events_dict
                    events_df, df = get_events_df(events_dict) #call get_events functionon the events_dict
                            # to get the dataframe, df, with all events
                    shots_df = df[df['isShot'] == True] #filtered dataframe to include only shots

                    shots_df['dist'] = "" #create new field for 'dist' distance from goal
                    shots_df['angle'] = "" #create new field for 'angle' from goal
                    shots_df['zone'] = "" #create new field for 'zone' on pitch

                    shots_df['country'] = country #field to store the country
                    shots_df['league'] = league #field to store the league
                    shots_df['year'] = year #field to store the year
                    shots_df['match'] = file.split(".")[0] #field to store match no

                    for index, row in shots_df.iterrows():
                        dist = get_shot_distance(row['x'], row['y'])#using co-ordinates call function to calculate distance
                        angle = get_shot_angle(row['x'], row['y'])#using co-ordinates call function to calculate angle
                        zone = get_pass_shot_zones(row['x'], row['y'])#using co-ordinates call function to calculate zone

                        shots_df['dist'].at[index] = dist #store distance
                        shots_df['angle'].at[index] = angle #store angle
                        shots_df['zone'].at[index] = zone #store zone
                    temp_df = pd.concat([temp_df, shots_df]) #combine shots_df from this match with the current temp_df
                    output_folder = f'{root}'
                    print(f'Output folder : {output_folder}')
                    output_file = f'{output_folder}/game_temp.csv'
                    temp_df.to_csv(output_file) #save temp file as we go along
                    count = count + 1
                    print(f'{country} : {league} : {year} : {file} complete')
                    prev_country = country
                    prev_league = league
                except:
                    pass

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
