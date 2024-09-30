import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
import warnings
import time
from datetime import datetime
import re

warnings.simplefilter('ignore')

my_date = time.strftime("%Y%m%d %H:%M:%S")
today = datetime.now()

print("Started at " + my_date)

folder_name = ''

f_path = '../GameData/'
f_name = f_path + 'ws_df_wsl2024.csv'
league = 'wsl'

### Run 1

fixtures_df = pd.DataFrame()

page_name = 'https://www.whoscored.com/Regions/252/Tournaments/739'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36'}
result = requests.get(page_name, headers=headers)
html_content = result.text
#print(text)

script_pattern = r'<script[^>]*>(.*?)</script>'

# Find all script contents
script_contents = re.findall(script_pattern, html_content, re.DOTALL)

performance_pattern = r'"performance":(.*?)require.config'

team_ids = []
names = []

# Iterate over all script contents and search for the performance pattern
for script_content in script_contents:
    matches = re.findall(performance_pattern, script_content, re.DOTALL)
    for match in matches:
        match = ',' + match
        teams = match.split("]")
        for team in teams:
            if len(team.split(",")) >= 4:
                team_id = team.split(",")[2]
                name = team.split(",")[3].replace("'", "")
                team_ids.append(team_id)
                names.append(name)

print(team_ids)
print(names)

columns=['country', 'date', 'Web_Address', 'Downloaded']
fix_df = pd.DataFrame(columns=columns)

for teamNo in team_ids:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36'}


    page_name = "https://www.whoscored.com/Teams/" + str(teamNo) + "/Fixtures/"
    result = requests.get(page_name, headers=headers)
    content = result.text
    #print(content)
    begin = 'fixtureMatches: ['
    end = '<script async type="text/javascript" data-main'

    idx1 = content.index(begin)
    idx2 = content.index(end)

    # length of substring 1 is added to
    # get string from next character
    res = content[idx1 + len(begin) + 1: idx2 - 21]
    res = ',[' + res
    # printing result
    print("The extracted string : " + res)
    time.sleep(5)

    split_res = res.split(',[')
    for s in split_res:
        if len(s.split(',')) >= 3:
            new_lst = s.split(',')
            web_address = f'https://www.whoscored.com/Matches/{new_lst[0]}/Live'
            date = new_lst[2].replace("'", "")
            new_row = pd.DataFrame({'country':league,'Web_Address':web_address, 'date':date}, index=[0])
            fix_df = pd.concat([fix_df, new_row])


print(fix_df)
fix_df.to_csv(f_name)
