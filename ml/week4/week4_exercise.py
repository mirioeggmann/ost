"""
Week4: build a linear regression model with help of sklearn and smf

26.09.2019 / Sascha Jecklin

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression


def lin_reg_with_sklearn(x, y):
    """
    Perform a simple linear regression with sklearn's LinearRegression

    Parameters
    ----------
    x : array_like
        The training data, given as 1-D array
    y : array_like
        The labels for the data given in 'x', as 1-D array

    Returns
    -------
    intercept : scalar
                beta_0 coefficient
    slope : scalar
            beta_1 coefficient
    """

    # TODO: Create a linear regression model and fit it to the data.
    # TODO: Return intercept and slope

    return intercept, slope


def reg_with_smf(data, formula_str: str):
    """
    Perform a regression with statsmodels' formula api. Print a summary of
    the coefficnets statistics.

    Parameters
    ----------
    data : pandas_data_frame
           The training data, given as matrix
    formula_str : string
                  The formula in R style which describes the model

    Returns
    -------
    params : array_like
             The regression coefficients as pandas_data_frame
    """

    # TODO: Create a ordinary least square model with smf and pass the
    # advertising data and a formula.
    # TODO: Print a summary of the coefficnets statistics.
    # TODO: Return the parameters.

    return params


def my2dplot(x, y, intercept, slope):
    """
    Plot the data and the regression line.

    Parameters
    ----------
    x : array_like
        The training data, given as 1-D vector
    y : array_like
        The labels for the data given in 'x', as 1-D array
    intercept : scalar
                The intercept of the regression line
    slope : scalar
            The slope of the interception line
    """

    # TODO: Plot x and y of a dataset.
    # TODO: Plot the regression line for this dataset.


def main(data_path):
    # reading data with pandas
    advertising = pd.read_csv(data_path, usecols=[1, 2, 3, 4])

    # TODO: call lin_reg_with_sklearn with correct parameters to create a linear
    # model which predicts sales based on TV budget using sklearn.

    # TODO: call reg_with_smf with correct parameters to create a linear model
    # which predicts sales based on TV budget using statsmodels.

    # TODO: plot the data set and the regression line for both results
    # (sklearn and smf). Use your my2dplot() function.

    # TODO: call reg_with_smf with correct parameters to create a linear model
    # which predicts sales based on TV budget, radio budget and the interaction
    # between radio and TV budget

    # TODO: calculated the correlation coefficient between all predictors
    # of the advertising data set and print it


if __name__ == '__main__':
    main('Advertising.csv')
    # main('Boston.csv')
