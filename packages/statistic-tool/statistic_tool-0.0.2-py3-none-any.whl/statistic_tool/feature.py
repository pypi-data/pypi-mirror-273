import pandas as pd
import numpy as np

def calculate_iv(dataframe, feature, target):
    """
    Calculate the Information Value (IV) of a feature.
    
    Args:
    dataframe (pd.DataFrame): The DataFrame containing the feature and target.
    feature (str): The name of the feature column.
    target (str): The name of the target column.
    
    Returns:
    float: The Information Value of the feature.
    """
    # Create a temporary DataFrame with feature and target
    temp_df = dataframe[[feature, target]].copy()
    
    # Handle missing values by treating them as a separate category
    temp_df[feature] = temp_df[feature].fillna("Missing")
    
    # Calculate the total counts of goods and bads
    total_goods = temp_df[target].sum()
    total_bads = len(temp_df[target]) - total_goods
    
    # Group by feature and calculate the necessary statistics
    grouped_df = temp_df.groupby(feature)[target].agg(['count', 'sum'])
    grouped_df.columns = ['TotalCount', 'GoodCount']
    grouped_df['BadCount'] = grouped_df['TotalCount'] - grouped_df['GoodCount']
    
    # Calculate the percentages for goods and bads
    grouped_df['GoodPercent'] = grouped_df['GoodCount'] / total_goods
    grouped_df['BadPercent'] = grouped_df['BadCount'] / total_bads
    
    # Calculate WOE and IV
    grouped_df['WOE'] = np.log(grouped_df['GoodPercent'] / grouped_df['BadPercent'])
    grouped_df['IV'] = (grouped_df['GoodPercent'] - grouped_df['BadPercent']) * grouped_df['WOE']
    
    # Handle any infinities or NaNs from log(0) or division by zero
    grouped_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    
    # Sum up IV for the feature
    iv_value = grouped_df['IV'].sum()
    
    return iv_value

def iv_table(dataframe, target):
    """
    Generate a table of IV values for all features in the DataFrame.
    
    Args:
    dataframe (pd.DataFrame): The DataFrame containing the features and target.
    target (str): The name of the target column.
    
    Returns:
    pd.DataFrame: A DataFrame with features and their IV values.
    """
    iv_values = {}
    for column in dataframe.columns:
        if column != target:  # Exclude the target variable
            iv_values[column] = calculate_iv(dataframe, column, target)
    
    return pd.DataFrame.from_dict(iv_values, orient='index', columns=['IV']).sort_values(by='IV', ascending=False)
