# Basic imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split  
from scipy import stats

# Scalers
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

#---------------------------------------------------------------------------------------------------------

# Function for Training, Validating, and Testing the data. 
def split_data(df, target= 'enter target column here'):
    ''' 
        This function is the train, validate, test, function.
        1. First we create the TRAIN and TEST dataframes at an 0.80 train_size( or test_size 0.2).
        2. Second, use the newly created TRAIN dataframe and split that at a 0.70 train_size
        ( or test_size 0.3), which means 70% of the train dataframe, so 56% of all the data.
        Now we have a train, validate, and test dataframes
    '''
    train, test = train_test_split(df, train_size=0.8, random_state=123, stratify=df[target])
    train, validate = train_test_split(train, train_size = 0.7, random_state = 123, stratify=train[target])
    return train, validate, test

#---------------------------------------------------------------------------------------------------------

def convert_percent_cols(df):
    
    # Remove '%' and convert to Float
    df.win_percentage = df.win_percentage.str.replace('%','').astype(float)
    df.ko_percentage = df.ko_percentage.str.replace('%','').astype(float)
    df.ko_against_percentage = df.ko_against_percentage.str.replace('%','').astype(float)
    
    # Lists to hold numbers
    win_percentage_list = []
    ko_percentage_list = []
    ko_against_percentage_list = []
    
    # Loop for win percentage
    for number in df.win_percentage:
        
        # Multiply to turn into decimal
        new = number * 0.01
        
        # Append lis
        win_percentage_list.append(new)
    
    # Loop for KO percentage
    for number in df.ko_percentage:
        
        # Multiply to turn into decimal
        new = number * 0.01
        
        # Append lis
        ko_percentage_list.append(new)
    
    # Loop for KO against percentage
    for number in df.ko_against_percentage:
        
        # Multiply to turn into decimal
        new = number * 0.01
        
        # Append lis
        ko_against_percentage_list.append(new)
        
    df['win_percentage'] = win_percentage_list
    df['ko_percentage'] = ko_percentage_list
    df['ko_against_percentage'] = ko_against_percentage_list
    
    return df


#---------------------------------------------------------------------------------------------------------

def convert_sec_col(df):
    

    # Remove 's' 
    df.avg_ko_time = df.avg_ko_time.str.replace('s','')
    
    # Replace NaN with '0'
    df.avg_ko_time = df.avg_ko_time.fillna(0)
    
    df.avg_ko_time = df.avg_ko_time.astype(float)
    
    return df

#---------------------------------------------------------------------------------------------------------
