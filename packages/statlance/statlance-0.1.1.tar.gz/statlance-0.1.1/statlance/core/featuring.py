#statlance\core\featuring.py
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import pandas as pd
import numpy as np
def data_process(df):
    """
    Function to perform data wrangling tasks.
    """
    # Perform any additional data wrangling tasks here
    df = missing_values(df)
    df = duplicates(df)
    df = conversion(df)
    df = engineering(df)
    df = normalization_scaling(df)
    df = encode_categorical(df)
    df = grouping_and_aggregation(df)
    df = reshape_data(df)
    df = merge_and_join(df)
    df = text_processing(df)
    df = pivot_tables(df)
    df = outliers(df)
    return df

def missing_values(df, columns=None, action='drop', value=None):
    """
    Function to handle missing values in specified columns or the entire DataFrame.
    
    Parameters:
        df (DataFrame): The input DataFrame.
        columns (list or str, optional): List of columns to consider for handling missing values.
                                          If None, the entire DataFrame is considered. Default is None.
        action (str, optional): Action to take when missing values are found. Possible values are 'drop' or 'replace'.
                                Default is 'drop'.
        value (any, optional): Value to replace missing values with if action is 'replace'. Default is None.
    
    Returns:
        DataFrame: The DataFrame with missing values handled according to the specified action.
    """
    if columns is None:
        columns = df.columns
    
    if action == 'drop':
        df.dropna(subset=columns, inplace=True)
    elif action == 'replace':
        df.fillna(value, inplace=True)
    else:
        raise ValueError("Invalid action. Supported actions are 'drop' and 'replace'.")
    
    return df



def duplicates(df, columns=None, action='drop', value=None):
    """
    Function to handle duplicates in specified columns or the entire DataFrame.
    
    Parameters:
        df (DataFrame): The input DataFrame.
        columns (list or str, optional): List of columns to consider for identifying duplicates.
                                          If None, the entire DataFrame is considered. Default is None.
        action (str, optional): Action to take when duplicates are found. Possible values are 'drop' or 'replace'.
                                Default is 'drop'.
        value (any, optional): Value to replace duplicates with if action is 'replace'. Default is None.
    
    Returns:
        DataFrame: The DataFrame with duplicates handled according to the specified action.
    """
    if columns is None:
        columns = df.columns
    
    if action == 'drop':
        df.drop_duplicates(subset=columns, inplace=True)
    elif action == 'replace':
        df.drop_duplicates(subset=columns, inplace=True)
        df.fillna(value, inplace=True)
    else:
        raise ValueError("Invalid action. Supported actions are 'drop' and 'replace'.")
    
    return df




def outliers(df, columns=None, method='remove', replace_with=None):
    """
    Function to handle outliers in specified columns or the entire DataFrame.
    
    Parameters:
        df (DataFrame): The input DataFrame.
        columns (list, optional): List of columns to handle outliers. If None, all numeric columns are selected.
        method (str, optional): The method to handle outliers. Supported methods: 'remove', 'replace'.
                                Default is 'remove'.
        replace_with (str, optional): The method to replace outliers if method is 'replace'. Supported methods:
                                       'mean', 'median', 'mode'. Default is None.
    
    Returns:
        DataFrame: The input DataFrame with outliers handled according to the specified method.
    """
    if columns is None:
        # If no columns are specified, handle outliers in all numeric columns in the DataFrame
        numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    else:
        # Handle outliers only in the specified columns
        numeric_cols = columns

    if method == 'remove':
        # Remove outliers
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    elif method == 'replace':
        # Replace outliers
        for col in numeric_cols:
            if replace_with == 'mean':
                df[col] = np.where(
                    (df[col] < df[col].quantile(0.25)) | (df[col] > df[col].quantile(0.75)),
                    df[col].mean(),
                    df[col]
                )
            elif replace_with == 'median':
                df[col] = np.where(
                    (df[col] < df[col].quantile(0.25)) | (df[col] > df[col].quantile(0.75)),
                    df[col].median(),
                    df[col]
                )
            elif replace_with == 'mode':
                df[col] = np.where(
                    (df[col] < df[col].quantile(0.25)) | (df[col] > df[col].quantile(0.75)),
                    df[col].mode()[0],
                    df[col]
                )
            else:
                raise ValueError("Unsupported replacement method. Supported methods: 'mean', 'median', 'mode'")

    return df


def conversion(df, columns=None, new_data_type='float64'):
    """
    Function to convert data types of specified columns or the entire DataFrame.
    """
    if columns is None:
        df = df.astype(new_data_type)
    else:
        df[columns] = df[columns].astype(new_data_type)
    return df



def engineering(df, techniques=None, columns=None):
    """
    Function to perform feature engineering on specified columns or the entire DataFrame.
    
    Parameters:
        df (DataFrame): The input DataFrame.
        techniques (dict, optional): Dictionary where keys represent feature engineering techniques
                                     and values represent corresponding columns. If None, no feature engineering
                                     is performed. Default is None.
        columns (list, optional): List of columns to perform feature engineering on. If None, all columns
                                  are considered. Default is None.
    
    Returns:
        DataFrame: The DataFrame with feature engineering applied.
    """
    if techniques is None:
        return df
    
    for technique, cols in techniques.items():
        if technique == 'binning':
            for col in cols:
                # Example: Bin numerical feature into categories
                df[col + '_binned'] = pd.cut(df[col], bins=3, labels=['low', 'medium', 'high'])
        elif technique == 'dummy_variables':
            for col in cols:
                # Example: Convert categorical feature into dummy variables
                df = pd.get_dummies(df, columns=[col], drop_first=True)
        elif technique == 'datetime_features':
            for col in cols:
                # Example: Extract year and month from datetime feature
                df[col + '_year'] = df[col].dt.year
                df[col + '_month'] = df[col].dt.month
        elif technique == 'text_features':
            for col in cols:
                # Example: Extract word count from text feature
                df[col + '_word_count'] = df[col].apply(lambda x: len(x.split()))
        elif technique == 'interaction_features':
            # Example: Create interaction feature by multiplying two existing features
            for col1, col2 in cols:
                df[col1 + '_' + col2 + '_interaction'] = df[col1] * df[col2]
        elif technique == 'log_transformation':
            for col in cols:
                # Example: Apply log transformation to numerical feature
                df[col + '_log'] = np.log(df[col])
        elif technique == 'scaling':
            for col in cols:
                # Example: Min-Max scaling of numerical feature
                df[col + '_scaled'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        elif technique == 'polynomial_features':
            for col in cols:
                # Example: Create polynomial feature
                df[col + '_squared'] = df[col] ** 2
        elif technique == 'grouping_and_aggregation':
            for col in cols:
                # Example: Aggregate feature across groups
                df[col + '_mean_group'] = df.groupby(col)['target'].transform('mean')
        elif technique == 'cross_features':
            # Example: Create cross feature
            for col1, col2 in cols:
                df[col1 + '_' + col2] = df[col1] * df[col2]
    
    return df




def normalization_scaling(df, columns=None, method='min_max'):
    """
    Function to normalize or scale specified columns or the entire DataFrame.
    
    Parameters:
        df (DataFrame): The input DataFrame.
        columns (list, optional): List of columns to normalize or scale. If None, all numeric columns are selected.
        method (str, optional): The normalization method to use. Supported methods: 'min_max', 'z_score', 'robust'.
                                 Default is 'min_max'.
    
    Returns:
        DataFrame: The input DataFrame with the selected columns normalized or scaled.
    """
    if columns is None:
        # If no columns are specified, scale all numeric columns in the DataFrame
        numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    else:
        # Scale only the specified columns
        numeric_cols = columns

    # Initialize scaler based on selected method
    if method == 'min_max':
        scaler = MinMaxScaler()
    elif method == 'z_score':
        scaler = StandardScaler()
    elif method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError("Unsupported normalization method. Supported methods: 'min_max', 'z_score', 'robust'")

    # Scale the selected columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df




def encode_categorical(df, columns=None):
    """
    Function to encode categorical variables in specified columns or the entire DataFrame.
    """
    if columns is None:
        # If no columns are specified, encode all categorical columns in the DataFrame
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    else:
        # Encode only the specified columns
        categorical_cols = columns

    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols)

    return df_encoded


def grouping_and_aggregation(df, columns=None, by=None):
    """
    Function to perform grouping and aggregation on specified columns or the entire DataFrame.
    """
    if columns is None:
        # If no columns are specified, perform aggregation on the entire DataFrame
        grouped_df = df.groupby(by).agg('mean')  # Example aggregation using mean
    else:
        # If columns are specified, perform aggregation on those columns
        grouped_df = df.groupby(by)[columns].agg('mean')  # Example aggregation using mean
    
    return grouped_df


def reshape_data(df, columns=None, reshape_type='pivot', index=None, columns_to_pivot=None, values=None):
    """
    Function to reshape data in specified columns or the entire DataFrame.
    """
    if reshape_type == 'pivot':
        # Perform pivot operation
        if index is None or columns_to_pivot is None or values is None:
            raise ValueError("For pivot operation, 'index', 'columns_to_pivot', and 'values' must be specified.")
        df = df.pivot_table(index=index, columns=columns_to_pivot, values=values)
    elif reshape_type == 'stack':
        # Perform stack operation
        if columns is None:
            raise ValueError("For stack operation, 'columns' must be specified.")
        df = df.stack(columns)
    elif reshape_type == 'melt':
        # Perform melt operation
        if columns is None:
            raise ValueError("For melt operation, 'columns' must be specified.")
        df = df.melt(id_vars=columns)
    elif reshape_type == 'transpose':
        # Perform transpose operation
        df = df.transpose()
    else:
        raise ValueError("Invalid reshape_type. Supported values are 'pivot', 'stack', 'melt', and 'transpose'.")
    
    return df


def merge_and_join(df, other_df, on=None, how='inner'):
    """
    Function to merge and join the DataFrame with another DataFrame.
    """
    if on is None:
        # If 'on' parameter is not provided, perform a cross join
        merged_df = df.merge(other_df, how=how)
    else:
        # Perform merge based on specified columns
        merged_df = df.merge(other_df, on=on, how=how)
    return merged_df


def text_processing(df, columns=None, new_column_names=None):
    """
    Function to rename columns in specified columns or the entire DataFrame.
    """
    if columns is None:
        # Rename all columns
        if new_column_names is None:
            return df
        else:
            df.columns = new_column_names
    else:
        # Rename specified columns
        if new_column_names is None or len(columns) != len(new_column_names):
            return df
        else:
            for old_col, new_col in zip(columns, new_column_names):
                if old_col in df.columns:
                    df.rename(columns={old_col: new_col}, inplace=True)
    return df


def pivot_tables(df, index=None, columns=None, values=None, aggfunc='mean'):
    """
    Function to create pivot tables from the DataFrame.
    """
    # Create pivot table
    pivot_df = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)
    
    return pivot_df
