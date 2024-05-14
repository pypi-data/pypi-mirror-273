# statlance/tests/test_viz.py

import pandas as pd
import pytest
from statlance.core import viz

# Test data
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)

def test_histogram():
    # Test case for histogram visualization
    with pytest.raises(SystemExit):
        viz.histogram(df, 'A')  # Ensure that it's attempting to plot but not actually doing it

def test_boxplot():
    # Test case for box plot visualization
    with pytest.raises(SystemExit):
        viz.boxplot(df, 'B')  # Ensure that it's attempting to plot but not actually doing it

def test_scatterplot():
    # Test case for scatter plot visualization
    with pytest.raises(SystemExit):
        viz.scatterplot(df, 'A', 'B')  # Ensure that it's attempting to plot but not actually doing it


