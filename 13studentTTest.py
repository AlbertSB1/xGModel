import pandas as pd
import numpy as np
from scipy.stats import ttest_ind_from_stats

def calculatePValue(wsl_df_file, men_df_file, comparator):
    wsl_df = pd.read_csv(wsl_df_file)

    actual_goals = wsl_df.groupby('match')['isGoal'].apply(lambda x: x.sum())
    cumulative_xG = wsl_df.groupby('match')['xG'].sum()

    wsl_match_summary = pd.DataFrame({'ActualGoals':actual_goals, 'CumulativeXG':cumulative_xG})

    wsl_match_summary['Difference'] = wsl_match_summary['CumulativeXG'] - wsl_match_summary['ActualGoals']

    wsl_mean_diff = wsl_match_summary['Difference'].mean()
    wsl_std_dev = wsl_match_summary['Difference'].std()
    wsl_obs = len(wsl_match_summary)


    men_df = pd.read_csv(men_df_file)

    actual_goals = men_df.groupby('match')['isGoal'].apply(lambda x: x.sum())
    cumulative_xG = men_df.groupby('match')['xG'].sum()

    men_match_summary = pd.DataFrame({'ActualGoals':actual_goals, 'CumulativeXG':cumulative_xG})

    men_match_summary['Difference'] = men_match_summary['CumulativeXG'] - men_match_summary['ActualGoals']

    men_mean_diff = men_match_summary['Difference'].mean()
    men_std_dev = men_match_summary['Difference'].std()
    men_obs = len(men_match_summary)

    print(f'Comparison between WSL and {comparator}')

    print(f'WSL Mean Difference : {wsl_mean_diff}, WSL Std Dev : {wsl_std_dev}, WSL No of Obs : {wsl_obs}')
    print(f'Men Mean Difference : {men_mean_diff}, Men Std Dev : {men_std_dev}, Men No of Obs : {men_obs}')

    t_stat, p_value = ttest_ind_from_stats(
        mean1=wsl_mean_diff,
        std1=wsl_std_dev,
        nobs1=wsl_obs,
        mean2=men_mean_diff,
        std2=men_std_dev,
        nobs2=men_obs
    )

    print(f'T Statistic : {t_stat}, P Value : {p_value}')
    print()
    print()

calculatePValue('wsl_df2.csv', 'lg2_df.csv', 'League Two')

calculatePValue('wsl_df1.csv', 'lg1_df.csv', 'League One')

calculatePValue('wsl_df_all.csv', 'all_df.csv', 'All English Men')
