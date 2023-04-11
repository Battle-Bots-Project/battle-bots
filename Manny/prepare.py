def merge_matchup_history(stats_df, match_history_df):
    """
    Merges the final dataframe with the melted match history dataframe,
    filling missing values with data from both original columns.
    
    Args:
        stats_df (pd.DataFrame): The final dataframe containing match statistics.
        match_history_df (pd.DataFrame): The melted match history dataframe.
        
    Returns:
        pd.DataFrame: The merged dataframe.
    """
    # Merge the dataframes on RobotName and Year columns, keeping all values from stats_df
    # and filling missing values with values from match_history_df.
    joined_df = stats_df.merge(match_history_df, on=['RobotName', 'Year'], how='left')

    # Replace missing values in the Value column with the corresponding value from the other Value column.
    joined_df['Value'] = joined_df['Value_x'].fillna(joined_df['Value_y'])
    
    # Replace missing values in the Stats column with the corresponding value from the other Stats column.
    joined_df['Stats'] = joined_df['Stats_x'].fillna(joined_df['Stats_y'])
    
    # Drop the original Value_x and Value_y columns.
    joined_df.drop(['Value_x', 'Value_y'], axis=1, inplace=True)
    
    # Drop the original Stats_x and Stats_y columns.
    joined_df.drop(['Stats_x', 'Stats_y'], axis=1, inplace=True)
    
    # Return the merged dataframe.
    return joined_df

def clean_merged_robot_data(df):
    """
    Cleans a merged dataframe of robot statistics by removing unnecessary characters from the 'Value' column,
    renaming the 'Stats' column to include the unit of measurement, and converting 'Value' to floats where appropriate.
    
    Args:
    - df: Pandas dataframe of merged robot statistics
    
    Returns:
    - df: cleaned Pandas dataframe of merged robot statistics
    """
    
    # Create a boolean mask of rows where the 'Value' column ends with '%'
    mask_percent = df['Value'].str.endswith('%').fillna(False).astype(bool)
    
    # Check if the 'Value' column contains the percent symbol, if so, remove it and convert to float
    df.loc[mask_percent, 'Value'] = df[mask_percent]['Value'].str.rstrip('%').astype(float)/100
    
    # Create a boolean mask of rows where the 'Value' column matches the pattern: [number] s
    mask_seconds = df['Value'].str.match(r'^\d+ s$').fillna(False).astype(bool)
    
    # Check if the 'Value' column contains an 's', if so, remove it and convert to float
    df.loc[mask_seconds, 'Value'] = df[mask_seconds]['Value'].str.rstrip('s').astype(float)
    
    # Rename the 'Stats' column from 'Average knockout time' to 'Average knockout time (seconds)'
    df.loc[df['Stats'] == 'Average knockout time', 'Stats'] = 'Average knockout time (seconds)'
    
    return df
