# statlance/tests/test_featuring.py

import pandas as pd
import pytest
from statlance.core import featuring

# Test data
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)

def test_missing_values():
    # Test case for handling missing values
    df_missing_values = df.copy()
    df_missing_values.iloc[0, 0] = None  # Introduce missing value
    df_cleaned = featuring.missing_values(df_missing_values)
    assert df_cleaned.isnull().sum().sum() == 0, "Missing values not handled correctly"

def test_duplicates():
    # Test case for handling duplicates
    df_duplicates = pd.concat([df, df], ignore_index=True)  # Introduce duplicate rows
    df_cleaned = featuring.duplicates(df_duplicates)
    assert len(df_cleaned) == len(df), "Duplicates not handled correctly"

def test_outliers():
    # Test case for handling outliers
    df_outliers = df.copy()
    df_outliers.iloc[0, 0] = 1000  # Introduce outlier
    df_cleaned = featuring.outliers(df_outliers)
    assert df_cleaned.iloc[0, 0] != 1000, "Outliers not handled correctly"


