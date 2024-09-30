import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
warnings.simplefilter('ignore')

uri = "mongodb+srv://xxxxxx:yyyyyy@mongoplayers.xp8lika.mongodb.net/?retryWrites=true&w=majority&appName=MongoPlayers"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['xG']
collection = db['shots']

def shots():
    projection = {
        'isGoal': 1,
        'isShot': 1,
        'prevEventType': 1,
        'angle': 1,
        'bodyPart': 1,
        'x': 1,
        'match': 1,
        'country': 1,
        'league': 1,
        'year': 1,
        'assisted':1,
        'penalty':1,
        'dist':1,
        'zone':1,
        '_id': 0
    }

    query = {'isShot':True}
    match_records = list(collection.find(query, projection))
    df = pd.DataFrame(match_records)
    return df


c_df = pd.read_csv('../Root/shots.csv')

corr_df = c_df[['x', 'y', 'isGoal', 'prevEventType', 'angle', 'bodyPart', 'keyPass', 'freeKick', 'cross', 'assisted',
              'penalty', 'throughBall', 'prevPassType', 'dist', 'zone']]

columns_to_factorize = ['isGoal', 'prevEventType', 'bodyPart', 'keyPass', 'freeKick', 'cross', 'assisted',
              'penalty', 'throughBall', 'prevPassType', 'zone']

for column in columns_to_factorize:
    corr_df[column], _ = pd.factorize(corr_df[column])

print(corr_df)

correlation_matrix = corr_df.corr()

print(correlation_matrix)

plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.show()

#remove 'cross' and 'throughball'
corr_df = c_df[['x', 'y', 'isGoal', 'prevEventType', 'angle', 'bodyPart', 'keyPass', 'freeKick', 'assisted',
              'penalty', 'prevPassType', 'dist', 'zone']]

columns_to_factorize = ['isGoal', 'prevEventType', 'bodyPart', 'keyPass', 'freeKick', 'assisted',
              'penalty', 'prevPassType', 'zone']

for column in columns_to_factorize:
    corr_df[column], _ = pd.factorize(corr_df[column])

print(corr_df)

correlation_matrix = corr_df.corr()

print(correlation_matrix)

df = shots()
print(f'Total no. of records : {len(df)}')

summary_df = df.groupby(['country', 'league', 'year'])['match'].nunique().reset_index(name='unique_matches_count')
print(summary_df.to_string(index=False))

summary_df = df.groupby(['country', 'league'])['match'].nunique().reset_index(name='unique_matches_count')
print(summary_df.to_string(index=False))

plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.show()


#plot frequency of goal in shots
df['isGoal'].fillna(False, inplace=True)
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='isGoal', data=df, palette='pastel')
plt.title('Frequency of Goals')
plt.xlabel('Frequency')
plt.ylabel('Shots')
plt.show()
print(f'Shots : {len(df)}, Goals : {len(df[df['isGoal']==True])}, Ratio = {((len(df[df['isGoal']==True])/len(df))*100):.2f}%')

#plot frequency of penalties in shots
df['penalty'].fillna(False, inplace=True)
pen_df = df[(df['penalty']==True) | (df['penalty']==False)]
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='penalty', data=pen_df, palette='pastel')
plt.title('Frequency of Penalties Taken')
plt.xlabel('Frequency')
plt.ylabel('Shots')
plt.show()
shots_taken = len(df)
pen_taken_df = df[df['penalty']==True]
pens_taken = len(pen_taken_df)
print(f'Non Penalty Shots : {shots_taken - pens_taken}, Penalties : {pens_taken}, Ratio : {((pens_taken/(shots_taken - pens_taken))*100):.2f}%')


#plot frequency of penalties scored
pen_df = df[df['penalty'] == True]
pen_df['penalty'].fillna(False, inplace=True)
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='isGoal', data=pen_df, palette='pastel')
plt.title('Frequency of Penalties Scored')
plt.xlabel('Frequency')
plt.ylabel('Goals')
plt.show()
print(f'All Penalties : {len(pen_df)}, Goals : {len(pen_df[pen_df['isGoal']==True])}, '
      f'Successful Penalties : {((len(pen_df[pen_df['isGoal']==True]))/(len(pen_df))*100):.2f}%')

#plot frequency of penalties scored with right foot
pen_df = df[(df['penalty'] == True) & (df['bodyPart']== 'rightFoot')]
pen_df['penalty'].fillna(False, inplace=True)
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='isGoal', data=pen_df, palette='pastel')
plt.title('Frequency of Penalties Scored - Right Foot')
plt.xlabel('Frequency')
plt.ylabel('Goals')
plt.show()
print(f'Right Foot Penalties : {len(pen_df)}, Goals : {len(pen_df[pen_df['isGoal']==True])}, '
      f'Successful Penalties : {((len(pen_df[pen_df['isGoal']==True]))/(len(pen_df))*100):.2f}%')

#plot frequency of penalties scored with left foot
pen_df = df[(df['penalty'] == True) & (df['bodyPart']== 'leftFoot')]
pen_df['penalty'].fillna(False, inplace=True)
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='isGoal', data=pen_df, palette='pastel')
plt.title('Frequency of Penalties Scored - Left Foot')
plt.xlabel('Frequency')
plt.ylabel('Goals')
plt.show()
print(f'Left Foot Penalties : {len(pen_df)}, Goals : {len(pen_df[pen_df['isGoal']==True])}, '
      f'Successful Penalties : {((len(pen_df[pen_df['isGoal']==True]))/(len(pen_df))*100):.2f}%')



#plot frequency of body parts used in shots
df['bodyPart'].fillna(False, inplace=True)
plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
sns.countplot(y='bodyPart', data=df, palette='pastel')
plt.title('Frequency of Body Part Used')
plt.xlabel('Frequency')
plt.ylabel('Shots')
plt.show()

#Kernel Density Estimate plot of angle
sns.kdeplot(df['angle'], bw_adjust=0.5, fill=True)
plt.xlabel('Angle (degrees)')
plt.ylabel('Density')
plt.title('Density of Shots by Angle')
plt.xlim(0, 180)
plt.show()

#Kernel Density Estimate plot of distance
d_df = df[df['penalty'] != True]
sns.kdeplot(d_df['dist'], bw_adjust=0.5, fill=True)
plt.xlabel('Distance (metres)')
plt.ylabel('Density')
plt.title('Density of Shots by Distance')
plt.xlim(0, 100)
plt.show()

#Kernel Density Estimate plot of elapsed time in seconds
c_df = c_df[c_df['cumulative_seconds']<=7750]
sns.kdeplot(c_df['cumulative_seconds'], bw_adjust=0.5, fill=True)
plt.xlabel('Seconds')
plt.ylabel('Density')
plt.title('Density of Shots by Time (s)')
plt.xlim(0, 7750)
plt.show()

