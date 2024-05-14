# statlance/tests/test_stats.py

import pandas as pd
import numpy as np
import pytest
from statlance.core import stats

# Test data
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)

def test_summary_statistics():
    # Test case for summary statistics
    summary = stats.summary_statistics(df)
    assert 'A' in summary.columns and 'B' in summary.columns, "Summary statistics not computed correctly"

def test_correlation_matrix():
    # Test case for correlation matrix
    correlation = stats.correlation_matrix(df)
    assert correlation.shape == (2, 2), "Correlation matrix not computed correctly"

def test_t_test():
    # Test case for t-test
    group1 = df['A']
    group2 = df['B']
    t_statistic, p_value = stats.t_test(group1, group2)
    assert isinstance(t_statistic, float) and isinstance(p_value, float), "T-test not computed correctly"


