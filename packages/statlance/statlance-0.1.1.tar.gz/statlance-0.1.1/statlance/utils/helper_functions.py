
# statlance/utils/helper_functions.py

import pandas as pd
import numpy as np

def check_missing_values(df):
    """
    Check for missing values in a DataFrame.
    """
    missing_values = df.isnull().sum()
    return missing_values

def normalize_data(df):
    """
    Normalize numerical data in a DataFrame.
    """
    numerical_cols = df.select_dtypes(include=np.number).columns
    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].min()) / (df[numerical_cols].max() - df[numerical_cols].min())
    return df

def filter_outliers(df, threshold=3):
    """
    Filter outliers in numerical columns of a DataFrame.
    """
    numerical_cols = df.select_dtypes(include=np.number).columns
    for col in numerical_cols:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        df = df[z_scores < threshold]
    return df

def generate_sample_data(n_rows=100):
    """
    Generate sample data with random values.
    """
    data = {
        'A': np.random.randint(1, 100, size=n_rows),
        'B': np.random.randn(n_rows),
        'C': np.random.choice(['X', 'Y', 'Z'], size=n_rows),
        'D': pd.date_range('2022-01-01', periods=n_rows)
    }
    df = pd.DataFrame(data)
    return df
