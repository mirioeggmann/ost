# -*- coding: utf-8 -*-
# @Author: Simon Walser
# @Date:   2020-10-21 09:57:04
# @Last Modified by:   Simon Walser
# @Last Modified by:   Nicolas Tobler
# @Last Modified date: 2022-10-4

"""
Week 3: build a linear regression model using only NumPy

SOLUTION

06.05.2019 / Hannes Badertscher

"""
import numpy as np
from scipy.stats import t


def calculate_standard_errors(beta_0, beta_1, X, y):
    """ Calculates the standard errors of beta_0 and beta_1

    Using equation (3.8) from the book, the standard errors for
    the coefficients `beta_0` and `beta_1` are calculated. The
    residual standard error (RSE) is used as an estimate of
    the variance `epsilon`.

    Parameters
    ----------
    beta_0: the estimated coefficient for the intercept beta_0.
    beta_1: the estmiated coefficient for the input x.
    X : array_like
        The data to estimate the standard errors on, given as a 2-D array.
        Usually, this will be the training data.
    y : array_like
        The labels corresponding to `X`

    Returns
    -------
    se_beta_0, se_beta_1: float
        The standard errors for beta_0 and beta_1

    """
    n_samples = y.size
    y_pred = beta_1 * X + beta_0

    residual_sum_squared = np.sum(np.square(y_pred - y))
    print(residual_sum_squared)
    residual_standard_error = np.sqrt(residual_sum_squared / (n_samples - 2))
    print(residual_standard_error)

    x_mean = np.mean(X)
    denominator = np.sum(np.square(X - x_mean))

    se_beta_0 = np.sqrt(np.square(residual_standard_error) *
                        (1 / n_samples + np.square(x_mean) / denominator))
    se_beta_1 = np.sqrt(np.square(residual_standard_error) / denominator)
    return se_beta_0, se_beta_1


def simple_linear_regression(X, y):
    """ Performs a simple linear regression with a single input feature

    Implement the linear regression with numpy and manually estimates
    the standard errors, t-, and p-values and prints them to the console.

    Parameters
    ----------
    X : array_like
        The training data, given as a 1-D array
    y : array_like
        The labels for the data given in `X`, as a 1-D array.

    """
    n_samples = y.size

    x_m = np.mean(X)
    y_m = np.mean(y)

    beta_1 = np.sum((X - x_m) * (y - y_m)) / np.sum(np.square(X - x_m))
    beta_0 = y_m - beta_1 * x_m

    print(f"beta_0:     {beta_0:8.4f}")
    print(f"beta_1:     {beta_1:8.4f}")

    se_beta_0, se_beta_1 = calculate_standard_errors(beta_0, beta_1, X, y)
    print(f"SE(beta_0): {se_beta_0:8.4f}")
    print(f"SE(beta_1): {se_beta_1:8.4f}")

    # Equation (3.14)
    t_beta_0 = beta_0 / se_beta_0
    t_beta_1 = beta_1 / se_beta_1
    print(f"t(beta_0):  {t_beta_0:8.4f}")
    print(f"t(beta_1):  {t_beta_1:8.4f}")

    # The factor 2 is due to using the two-sided t-test
    p_beta_0 = 2 * t.sf(np.abs(t_beta_0), n_samples - 2)
    p_beta_1 = 2 * t.sf(np.abs(t_beta_1), n_samples - 2)
    print(f"p(beta_0):  {p_beta_0:e}")
    print(f"p(beta_1):  {p_beta_1:e}")


def main(data_path):
    """ Main function which runs the linear regression on Advertising data """
    advertising_data = np.genfromtxt(data_path,
                                     delimiter=',',
                                     skip_header=True)

    tv_data = advertising_data[:, 1]
    sales_data = advertising_data[:, 4]

    simple_linear_regression(tv_data, sales_data)


if __name__ == '__main__':
    main('../Advertising.csv')
