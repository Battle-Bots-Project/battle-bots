import pandas as pd  
from selenium import webdriver
import json
import csv

def save_links_to_csv(links, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link])

def load_links_from_csv(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        links = [row[0] for row in reader]
    return links

def save_to_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def load_from_json(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def get_rid_of_cookies_popup(driver):
    # cookies alert window popup, close button
    cookies_button = driver.find_element_by_class_name("cmplz-close")
    
    # click close button
    cookies_button.click()

def get_season_links():
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
            season = class_element[i].find_elements_by_tag_name("a")[j+1].get_attribute("href")
            links.append(season)
    
    # getting link attribute for last item in list of class elements
    season = class_element[7].find_element_by_tag_name("a").get_attribute("href")
    
    # one final append for last item
    links.append(season)
    
    # close scraper browser
    driver.quit()
    
    return links

def get_season_robot_links(season_link):
    # start scraper with link
    driver = webdriver.Chrome()
    driver.get(season_link)
    
    links = []
    # go to season link
    driver.get(season_link)
    
    # get all robot overlay elements to list
    thumbnail_overlay_elements = driver.find_elements_by_css_selector(".portfolio-item-wrapper")
    
    # iterate through list of robot elements
    for thumbnail_overlay_element in thumbnail_overlay_elements:
        link_element = thumbnail_overlay_element.find_element_by_css_selector("a.button")
        link = link_element.get_attribute("href")
        links.append(link)
    
    # close scraper browser
    driver.quit()
    
    return links

def get_all_season_robot_links():
    # get the list of season links
    season_links = get_season_links()

    # dictionary to store robot links for each season
    all_season_robot_links = {}

    # iterate through the season links
    for season_link in season_links:
        # extract the season name from the URL
        season_name = season_link.split('/')[-2]

        # get the list of robot links for the current season
        robot_links = get_season_robot_links(season_link)

        # add the robot links to the dictionary with the season name as the key
        all_season_robot_links[season_name] = robot_links

    return all_season_robot_links

def get_all_wiki_robot_links():
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
    
    # iterate through all the alplhabet class member and extract `css` element which has link
    for member_element in member_elements:
        a_elements = member_element.find_elements_by_css_selector(".category-page__member-link")
        
        # get the link in every alphabet `css` element link
        for a_element in a_elements:
            
            # append to the empty list
            links.append(a_element.get_attribute("href"))
            
    return links

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
