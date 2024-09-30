import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
import warnings
import time
from datetime import datetime
from datetime import timedelta
from json_functions_v2 import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

leagues = {'Liga Professional':{'country':'Argentina', 'fixtures':'ws_df_argentina.csv'},
           'Jupiler Pro League':{'country':'Belgium', 'fixtures':'ws_df_belgium.csv'},
            'Bundesliga':{'country':'Germany', 'fixtures':'ws_df_germany1.csv'},
            'Bundesliga2':{'country':'Germany', 'fixtures':'ws_df_germany2.csv'},
            'WSL':{'country':'England', 'fixtures':'ws_df_wsl_2023.csv'},
            'Premier League':{'country':'England', 'fixtures':'ws_df_england_prem.csv'},
            'Championship':{'country':'England', 'fixtures':'ws_df_championship.csv'},
            'League One':{'country':'England', 'fixtures':'ws_df_efl1.csv'},
            'League Two':{'country':'England', 'fixtures':'ws_df_efl2.csv'},
            'Brasileirao':{'country':'Brazil', 'fixtures':'ws_df_brazil.csv'},
            'Ligue 1':{'country':'France', 'fixtures':'ws_df_france.csv'},
            'Serie A':{'country':'Italy', 'fixtures':'ws_df_italy.csv'},
            'Eredivisie':{'country':'Netherlands', 'fixtures':'ws_df_netherlands.csv'},
            'Liga Portugal':{'country':'Portugal', 'fixtures':'ws_df_portugal.csv'},
            'Russia Premier League':{'country':'Russia', 'fixtures':'ws_df_russia.csv'},
            'Premiership':{'country':'Scotland', 'fixtures':'ws_df_scotland.csv'},
            'LaLiga':{'country':'Spain', 'fixtures':'ws_df_spain.csv'},
            'Super Lig':{'country':'Turkey', 'fixtures':'ws_df_turkey.csv'},
            'MLS':{'country':'USA', 'fixtures':'ws_df_usa.csv'}}

warnings.simplefilter('ignore')

my_date = time.strftime("%Y%m%d %H:%M:%S")
today = datetime.now()
yesterday = today - timedelta(hours = 24)

year = '2023'

print("Started at " + my_date)

for league in leagues:
    if league == 'WSL':
        print(f'Processing league : {league}')

        folder_name = leagues[league]['country']

        f_path = f'../GameData/{folder_name}/{league}/{year}/'

        fixture_path = '../GameData/Fixtures/'
        f_name = f'{fixture_path}{leagues[league]["fixtures"]}'


        web_adds = pd.read_csv(f_name, index_col=0)

        for index, row in web_adds.iterrows():


            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36'}

            #country = row['Comp']
            #country = country.split('-')[0]

            try:
                yy = row['date'].split('/')[2]
                mm = row['date'].split('/')[1]
                dd = row['date'].split('/')[0]
                comp_date = datetime(int(yy), int(mm), int(dd))
            except:
                comp_date = datetime(2024,12,31)
            if comp_date < (yesterday) and str(row['Downloaded'])!= 'True':
                print(str(comp_date) + " < " + str(yesterday) + " AND Downloaded = " + str(row['Downloaded']))

                page_name = row['Web_Address']
                country = row['country']
                print(page_name)

                driver.get(page_name)

                result = driver.get(page_name)
                content = driver.page_source
                #driver.close()

                match_no = page_name.split('/')[4]

                f = f_path  + "" + str(match_no) + '.html'
                error_f = f_path + 'Error.txt'

                try:
                    file = open(f, 'w', encoding="utf-8")
                    file.write(content)
                    file.close()
                    if os.path.getsize(f) > 500000:
                        print("File 1  : " + str(match_no) + " written at " + time.strftime("%Y%m%d %H:%M:%S"))
                        web_adds['Downloaded'].at[index] = True
                    else:
                        os.remove(f)

                except:
                    print(str(match_no) + " not written")
                    try:
                        file = open(error_f, 'a', encoding="utf-8")
                    except:
                        file = open(error_f, 'w', encoding="utf-8")

                    file.write(str(match_no) + " not written \n")
                    file.close()

                time.sleep(15)
            else:
                pass
        web_adds.to_csv(f_name)


print("Finished at " + time.strftime("%Y%m%d %H:%M:%S"))
