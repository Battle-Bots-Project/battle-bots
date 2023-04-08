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
