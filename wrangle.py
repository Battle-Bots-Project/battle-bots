i#basic data science imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# JSON and Regex
import json
import re

# Scraping imports
import nltk
from requests import get
from bs4 import BeautifulSoup

#------------------------------------------------------------------------------------------------------------

def all_teams_2021():
    
    """
    Returns a Pandas DataFrame that contains the statistics of the robots from the 2021 season of BattleBots.

    The function loads a JSON file named 'all_season_robot_links.json' that contains a list of URLs for all the robots
    in the history of BattleBots. It then filters out the URLs of robots from the 2021 season and creates an empty 
    DataFrame with columns to store the stats.

    """

    
    # Load JSON file 
    with open('all_season_robot_links.json') as json_file:
        data = json.load(json_file)
    
    # List URLs for robots from season 2021. Acquired from JSON file
    bots_2021 = data['2021-season-robots']
    
     # Create an empty dataframe to store the stats
    df = pd.DataFrame(columns=['total_matches', 'win_percentage', 'total_wins', 'losses', 'ko',\
                               'ko_percentage', 'avg_ko_time', 'ko_against', 'ko_against_percentage',\
                               'decision_wins'])
    
    # List of names
    name_list = []
    
    # Iterate through list of robots
    for bot in bots_2021:
        
        # URL
        robot = pd.read_html(bot)
        
        # Stat History Table from battlebots.com
        robot = robot[0]
        
        # Regex to get bot name from URL and append to list
        robot_name =  re.search(r'/([^/]+)/?$', bot)[0]
        name_list.append(robot_name)
        
        # Getting all stats from Career column
        stats_list = []
        
        # Iterate through Career column
        for i in robot.Career:
            # append values 
            stats_list.append(i)
        
        print(bot) 
        
        # Append stats to dataframe
        df = df.append(pd.Series(stats_list, index=df.columns), ignore_index=True)
        
    # Create name column in dataframe
    df['robot_name'] = name_list

    # Remove '/' from name
    df.robot_name = df.robot_name.str.replace('/','')
    
    # Replace '-' with '_'
    df.robot_name = df.robot_name.str.replace('-','_')
    
    # Name list cleaned
    cleaned_names = []
    
    for name in df.robot_name:
        
        # Append cleaned names
        cleaned_names.append(name[:-5])
    
    # Cleaned up names
    df.robot_name = cleaned_names
    
    # Set robot_name column as Index
    df = df.set_index('robot_name')
        
    # Reset Index
    df = df.reset_index()
    
        
    return df

#------------------------------------------------------------------------------------------------------------