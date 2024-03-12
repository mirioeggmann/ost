"""
SOLUTION

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

    regr = LinearRegression()
    regr.fit(x.to_numpy().reshape([-1,1]), y)
    
    return regr.intercept_, regr.coef_


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

    mdl = smf.ols(formula=formula_str, data=data).fit()
    print(mdl.summary().tables[1])
    
    return mdl.params


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

    xi = np.linspace(np.min(x), np.max(x), 10)
    line = xi*slope+intercept
    plt.figure()
    plt.plot(x, y, 'o', xi, line)
    plt.show()


def main(data_path):
    # reading data with pandas
    advertising = pd.read_csv(data_path, usecols=[1, 2, 3, 4])
    
    # Perform regression with sklearn
    b0_1, b1_1 = lin_reg_with_sklearn(advertising.TV, advertising.sales)

    # Perform regression with smf
    b0_2, b1_2 = reg_with_smf(advertising, 'sales ~ TV')

    # Plot the data set and the regression line for both results
    my2dplot(advertising.TV, advertising.sales, b0_1, b1_1)
    my2dplot(advertising.TV, advertising.sales, b0_2, b1_2)

    # Create a linear model which regresses sales onto TV budget,
    # radio budget and the interaction betwenn radio and TV budget
    params = reg_with_smf(advertising, 'sales ~ TV+radio+radio*TV')

    # Print correlation coefficient between all predictor variables and
    # the response variable.
    print(advertising.corr())


if __name__ == '__main__':
    main('Advertising.csv')
    # main('Boston.csv')
