"""
Week9: Feature selection and regression

12.11.2019 / Sascha Jecklin

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler

###############################################################################
##
## Functions
##
###############################################################################

def best_subset(x, y):
    """ Carries out a best subset selection of features for a
        LinearRegression model
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    # TODO:
    pass


def forward_selection(x, y):
    """ Carries out a forward stepwise selection of features for a
        LinearRegression model
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    # TODO:
    pass


def ridge_regression(x, y):
    """ Fits a linear regression model with different L2 regularization terms
        and plots the model coefficients depending on lambda (alpha)
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    # TODO:
    pass


def lasso_regression(x, y):
    """ Fits a linear regression model with different L1 regularization terms
        and plots the model coefficients depending on lambda (alpha)
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    # TODO:
    pass


def fit_linear_reg(x, y):
    """ Fits a linear regression model

    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels

    Returns:
    --------
    r_squared: float
               r^2 values
    adj_r_squared: float
                   adjusted r^2 values
    """
    mdl = LinearRegression()
    mdl.fit(x, y)
    r_squared = mdl.score(x, y)
    adj_r_squared = 1 - (1 - r_squared) * (y.shape[0] - 1) / (y.shape[0] - x.shape[1] - 1)

    return r_squared, adj_r_squared

###############################################################################
##
## Main
##
###############################################################################

def main(data_path):
    # read data and remove NaN
    dataset = pd.read_csv(data_path).dropna()

    # convert categorical data into numbers
    dataset = pd.get_dummies(dataset, columns=['Gender', 'Student', 'Married',
                                               'Ethnicity'], drop_first=True)

    y = dataset.Balance
    x = dataset.drop(columns='Balance', axis=1)  # everything without balance

    # calling the four task functions
    best_subset(x, y)
    forward_selection(x, y)
    ridge_regression(x, y)
    lasso_regression(x, y)


if __name__ == '__main__':
    main(data_path='Credit.csv')
