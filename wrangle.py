i#basic data science imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# JSON and Regex
import json
import re

# Time and OS
import time 
import os 

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

def stats_df():
    """
    A function that reads robot statistics from a list of links to web pages,
    filters and formats them to fit into a Pandas DataFrame, and concatenates all the resulting
    DataFrames into one master DataFrame.
    This uses a file named 'all_season_robot_links.json'

    Returns:
    --------
    Pandas DataFrame:
        A DataFrame containing robot statistics from all the links in the provided JSON file.
    """
    
    # read in the JSON file containing the robot web page links
    with open('all_season_robot_links.json') as json_file:
        data = json.load(json_file)

    # create an empty DataFrame to store concatenated tables
    all_tables = pd.DataFrame()

    # loop through every key in data
    for key in data.keys():

        print(f"Scraping statistics for {key} robots...")

        # loop through every link associated with the current key
        for i in data[key]:

            print(f"\tScraping {i}...")

            # try to read tables from the current link
            try:
                tables = pd.read_html(i)

            # if no tables are found, skip to the next link
            except ValueError:
                continue

            # try to format the first table in the resulting list of tables
            try:
                # select and transpose the relevant rows from the table
                table = tables[0][['Stats', 'Career']].T

                # use the first row as column names
                table.columns = table.iloc[0]

                # drop the now redundant row of column names
                table = table.drop(index='Stats')

                # reset the row index to start from 0
                table = table.reset_index(drop=True)

                # extract the robot name from the current link and add it as a column to the table
                url = f'{i}'
                match = re.search(r'/([^/]+)/?$', url)
                if match:
                    table['robot'] = match.group(1)

            # if any errors occur while formatting the table, skip to the next link
            except KeyError:
                continue

            # add the current table to the master DataFrame
            all_tables = pd.concat([all_tables, table], ignore_index=True, axis=0)
            print(f"\t\t...table added to master DataFrame ({all_tables.shape[0]} rows)")

            # pause briefly to avoid overloading the web server with requests
            time.sleep(1)

    print("...done!")
    # return the completed master DataFrame
    # save to csv
    all_tables.to_csv('all-table1.csv'')
    return all_tables

#------------------------------------------------------------------------------------------------------------