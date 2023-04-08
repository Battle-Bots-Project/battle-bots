import os
import csv
import pandas as pd
from acquire import *
import re

def load_links_from_csv(filename):
    """
    Load a list of links from a CSV file.
    
    :param filename: The name of the CSV file to load the links from.
    :return: A list of links (strings) loaded from the CSV file.
    """
    # Open the CSV file in read mode with newline=''
    with open(filename, 'r', newline='') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        
        # Iterate through each row in the CSV file and extract the link (first element of each row)
        links = [row[0] for row in reader]

    # Return the list of links
    return links

def save_links_to_csv(links, filename):
    """
    Save a list of links to a CSV file.
    
    :param links: A list of links (strings) to be saved.
    :param filename: The name of the CSV file to save the links.
    """
    # Open the CSV file in write mode with newline=''
    with open(filename, 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        
        # Iterate through each link in the list
        for link in links:
            # Write the link as a row in the CSV file
            writer.writerow([link])

def load_from_json(file_name):
    """
    Load data from a JSON file.
    
    :param file_name: The name of the JSON file to load the data from.
    :return: The data loaded from the JSON file.
    """
    # Open the JSON file in read mode
    with open(file_name, 'r') as file:
        # Load the data from the JSON file
        data = json.load(file)
    
    # Return the loaded data
    return data

def save_to_json(data, file_name):
    """
    Save data to a JSON file.
    
    :param data: The data to be saved in JSON format.
    :param file_name: The name of the JSON file to save the data to.
    """
    # Open the JSON file in write mode
    with open(file_name, 'w') as file:
        # Dump the data into the JSON file
        json.dump(data, file)

def get_rid_of_cookies_popup(driver):
    """
    Close the cookies pop-up on the BattleBots website.
    
    :param driver: The WebDriver instance navigating the website.
    """
    # Find the cookies alert close button element by its class name
    cookies_button = driver.find_element_by_class_name("cmplz-close")
    
    # Click the close button to get rid of the cookies pop-up
    cookies_button.click()

def get_season_links():
    """
    Scrapes the BattleBots website to get the links for each season.

    :return: A list of links for each season.
    """
    # start scraper with link
    base_link = "https://battlebots.com/robots/"
    driver = webdriver.Chrome()
    driver.get(base_link)
    
    # get all season elements to list
    class_element = driver.find_elements_by_class_name("row")

    # list to save all links
    links = []

    # items 4 - 6 have 2 links, so using nested loop to get each
    for i in range(4, 7):
        for j in range(2):
            # extract the link for the current season and append it to the list of links
            season = class_element[i].find_elements_by_tag_name("a")[j+1].get_attribute("href")
            links.append(season)
    
    # extract the link for the final season and append it to the list of links
    season = class_element[7].find_element_by_tag_name("a").get_attribute("href")
    links.append(season)
    
    # close scraper browser
    driver.quit()
    
    return links

def get_season_robot_links(season_link):
    """
    Given a link to a BattleBots season page, this function returns a list of links to all the robots 
    that competed in that season.
    
    :param season_link: A string representing the URL of the BattleBots season page.
    :return: A list of strings representing the URLs of each robot that competed in the specified season.
    """
    # Start the scraper with the given link
    driver = webdriver.Chrome()
    driver.get(season_link)
    
    # Initialize an empty list to store the robot links
    links = []
    
    # Go to the season link
    driver.get(season_link)
    
    # Get all the robot overlay elements as a list
    thumbnail_overlay_elements = driver.find_elements_by_css_selector(".portfolio-item-wrapper")
    
    # Iterate through the list of robot elements
    for thumbnail_overlay_element in thumbnail_overlay_elements:
        # Extract the link element for the robot
        link_element = thumbnail_overlay_element.find_element_by_css_selector("a.button")
        # Get the link attribute for the robot and append it to the list of links
        link = link_element.get_attribute("href")
        links.append(link)
    
    # Close the scraper browser
    driver.quit()
    
    # Return the list of robot links
    return links

def get_all_season_robot_links_dict():
    """
    Scrape all season links and their associated robot links from the BattleBots website.

    :return: A dictionary containing season names as keys and lists of robot links as values.
    """
    # Get the list of season links
    season_links = get_season_links()

    # Dictionary to store robot links for each season
    all_season_robot_links_dict = {}

    # Iterate through the season links
    for season_link in season_links:
        # Extract the season name from the URL
        season_name = season_link.split('/')[-2]

        # Get the list of robot links for the current season
        robot_links = get_season_robot_links(season_link)

        # Add the robot links to the dictionary with the season name as the key
        all_season_robot_links_dict[season_name] = robot_links

    return all_season_robot_links_dict

def read_pickles_in_directory(directory_path):
    """
    Given a directory path containing pickle files of robots' match history and stats, this function reads and 
    stores them in a dictionary.

    :param directory_path: The path of the directory containing the pickle files.
    :return: A dictionary containing robot names as keys and a nested dictionary with 'match_history' and 'stats' 
             DataFrames as values.
    """
    robot_dict = {}
    
    # regular expression pattern for extracting robot name and table type from filename
    regex_pattern = r'(.+)_((match_history)|(stats))\.pkl'

    # iterate through each file in the directory
    for filename in os.listdir(directory_path):
        # check if the filename matches the regex pattern
        match = re.match(regex_pattern, filename)
        if match:
            # extract the robot name and table type from the filename
            robot_name = match.group(1)
            table_type = match.group(2)
            key = robot_name

            # read the pickle file and store the DataFrame in the appropriate dictionary key
            with open(os.path.join(directory_path, filename), 'rb') as f:
                df = pd.read_pickle(f)
                if not df.empty:
                    if key in robot_dict:
                        robot_dict[key][table_type] = df
                    else:
                        robot_dict[key] = {table_type: df}

    return robot_dict

def create_long_format_stats_df(robot_dict):
    """
    Given a dictionary of robots containing their stats, this function creates a long format DataFrame.
    
    :param robot_dict: A dictionary containing robot names as keys and nested dictionaries with 'stats' DataFrames as values.
    :return: A DataFrame in long format containing robot names, years, stats, and values.
    """
    # Initialize an empty list to store individual long format DataFrames for each robot
    long_format_dfs = []

    # Iterate through each robot name and the nested dictionary in robot_dict
    for robot_name, nested_dict in robot_dict.items():
        # Check if the nested dictionary contains a 'stats' DataFrame
        if "stats" in nested_dict:
            # Extract the 'stats' DataFrame from the nested dictionary
            stats_df = nested_dict["stats"]
            
            # Filter out the 'index' row from the 'stats' DataFrame
            stats_df = stats_df[stats_df['Stats'] != 'index']
            
            # Add a new column to the 'stats' DataFrame with the robot name
            stats_df["RobotName"] = robot_name
            
            # Melt the 'stats' DataFrame into long format
            stats_df = stats_df.melt(id_vars=['RobotName', 'Stats'], var_name='Year', value_name='Value')
            
            # Append the melted DataFrame to the list of long format DataFrames
            long_format_dfs.append(stats_df)

    # Concatenate the list of DataFrames into a single DataFrame
    final_df = pd.concat(long_format_dfs, ignore_index=True)
    
    # Return the final DataFrame in long format
    return final_df

def create_long_format_matchup_history_df(robot_dict):
    """
    Takes a dictionary of robot information, and returns a Pandas DataFrame containing
    the match history for all robots in long format.
    
    Parameters:
    robot_dict (dict): A dictionary where the keys are robot names and the values
        are dictionaries containing information about the robot.
    
    Returns:
    all_match_history_df_melt (Pandas DataFrame): A formatted Pandas DataFrame in long format,
        containing the match history for all robots in the input dictionary.
    """
    # Create an empty list to store the formatted match history dataframes
    match_history_dfs = []
    
    # Loop through each robot in the robot_dict dictionary
    for robot_name, tables_dict in robot_dict.items():
        # Check if the 'match_history' key exists in the tables_dict
        if 'match_history' in tables_dict:
            # Extract the match_history dataframe for this robot
            match_history_df = tables_dict['match_history']
            # Add a RobotName column with the robot's name
            match_history_df['RobotName'] = robot_name
            # Rename the columns in match_history_df
            match_history_df.columns = [col + '_match_history' if col not in ['Season', 'RobotName'] else col for col in match_history_df.columns]
            
            # Append the formatted dataframe to the list
            match_history_dfs.append(match_history_df)
            
    # Concatenate all the formatted match history dataframes into a single dataframe
    all_match_history_df = pd.concat(match_history_dfs)

    # Remove double "_matchup_history" suffix
    all_match_history_df.columns = all_match_history_df.columns.str.replace('_match_history_match_history', '_match_history')

    # Melt the all_match_history_df table
    all_match_history_df_melt = pd.melt(
        all_match_history_df,
        id_vars=['Season', 'RobotName'],
        value_vars=['Round_match_history', 'Matchup_match_history', 'Results_match_history', 'Opponent_match_history'],
        var_name='Stats',
        value_name='Value'
    )
    all_match_history_df_melt = all_match_history_df_melt.rename(columns={'Season': 'Year'})

    # Fix null concatenation issues
    all_match_history_df_melt.dropna(subset=['Year', 'Value'], inplace=True)

    return all_match_history_df_melt

def get_all_wiki_robot_links():
    """
    Scrapes the Battlebots wiki to extract links to all competitor list templates, which contain links to robots.

    :return: A list of links to all competitor list templates.
    """
    # link for wiki
    link = "https://battlebots.fandom.com/wiki/Category:Competitor_list_templates"

    # start scraper with link
    driver = webdriver.Chrome()

    # go to link
    driver.get(link)

    # isolate alphabet letter element
    member_elements = driver.find_elements_by_class_name("category-page__members-wrapper")

    # temporary list
    links = []

    # iterate through all the alphabet class member and extract `css` element which has link
    for member_element in member_elements:
        a_elements = member_element.find_elements_by_css_selector(".category-page__member-link")

        # get the link in every alphabet `css` element link
        for a_element in a_elements:

            # append to the empty list
            links.append(a_element.get_attribute("href"))

    # close scraper browser
    driver.quit()

    return links


