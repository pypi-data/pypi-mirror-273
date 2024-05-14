#statlance\core\stats.py
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go

def analyze_data(df):
    """
    Function to perform statistical analysis on the data.
    """
    print("Statlance - Statistical Analysis")
    
    # Display basic statistics
    print("Basic Statistics")
    print(df.describe())

def summary_statistics(df):
    """
    Function to compute summary statistics for the DataFrame.
    """
    return df.describe()

def correlation_matrix(df):
    """
    Function to compute the correlation matrix between variables.
    """
    return df.corr()

def t_test(group1, group2, equal_var=True):
    """
    Function to perform t-test for comparing means of two groups.
    
    Parameters:
    - group1: First group for comparison.
    - group2: Second group for comparison.
    - equal_var: (Optional) Whether to assume equal variance (default: True).
    
    Returns:
    - t_statistic: The calculated t-statistic.
    - p_value: The two-tailed p-value.
    """
    t_statistic, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)
    return t_statistic, p_value


def anova(df, groups, variable):
    """
    Function to perform ANOVA for comparing means of multiple groups.
    """
    model = sm.formula.ols(f"{variable} ~ C({groups})", data=df).fit()
    return sm.stats.anova_lm(model, typ=2)

def chi_square_test(df, column1, column2):
    """
    Function to perform chi-square test for independence.
    """
    contingency_table = pd.crosstab(df[column1], df[column2])
    return stats.chi2_contingency(contingency_table)

def linear_regression(df, X, y):
    """
    Function to perform linear regression.
    """
    X = sm.add_constant(df[X])  # Add constant term
    model = sm.OLS(df[y], X).fit()
    return model.summary()

def logistic_regression(df, X, y):
    """
    Function to perform logistic regression.
    """
    X = sm.add_constant(df[X])  # Add constant term
    model = sm.Logit(df[y], X).fit()
    return model.summary()

def k_means_clustering(df, n_clusters):
    """
    Function to perform K-means clustering.
    """
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(df)
    return kmeans.labels_

def pca(df, n_components):
    """
    Function to perform Principal Component Analysis (PCA).
    """
    from sklearn.decomposition import PCA
    pca = PCA(n_components=n_components)
    pca.fit(df)
    return pca.transform(df)

def mann_whitney_u_test(group1, group2):
    """
    Function to perform Mann-Whitney U test for comparing distributions.
    """
    return stats.mannwhitneyu(group1, group2)

def histogram(df, column):
    """
    Function to create histogram for data visualization.
    """
    fig = px.histogram(df, x=column)
    fig.show()

def boxplot(df, column):
    """
    Function to create box plot for visualizing distribution of data.
    """
    fig = px.box(df, y=column)
    fig.show()

def scatterplot(df, x, y):
    """
    Function to create scatter plot for visualizing relationships between variables.
    """
    fig = px.scatter(df, x=x, y=y)
    fig.show()
