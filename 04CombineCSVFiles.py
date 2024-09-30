import pandas as pd
import warnings
import os

root_dir = '../GameData/Root1'

shot_df = pd.DataFrame()
warnings.simplefilter('ignore')

for root, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('game_temp.csv'):
            path_parts = root.split(os.sep)
            # Ensure the path_parts list has enough elements to unpack
            if len(path_parts) >= 4:
                country, league, year = path_parts[-3:]
            import_df = pd.read_csv(f'{root}/{str(file)}')
            shot_df = pd.concat([shot_df, import_df], ignore_index=True)
            print(f'{file} complete')

shot_df.to_csv(f'{root_dir}/shots.csv')

num_rows = shot_df.shape[0]
num_cols = shot_df.shape[1]
print(f'Number of rows: {num_rows}')
print(f'Number of columns: {num_cols}')

shots = shot_df[shot_df['isShot'] == True].shape[0]
goals = shot_df[shot_df['isGoal'] == True].shape[0]

print(f'Shots : {shots}, Goals : {goals}')

duplicates = shot_df.duplicated().any()

# Check if there are any duplicates
if duplicates:
    print("There are duplicate rows in the DataFrame.")
else:
    print("There are no duplicate rows in the DataFrame.")
