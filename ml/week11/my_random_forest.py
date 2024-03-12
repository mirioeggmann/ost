"""
Week11: own random forest implementation

26.11.2019 / Sascha Jecklin

"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


class MyRandomForestClassifier():
    """ Implementation of a RandomForestClassifier using DecisionTreeClassifier

    Parameters
    ----------
    int : max_depth
          max depth of the threes
    int : n_estimators
          number of trees in the forest

    Methods
    -------
    fit(x, y)
        Fits classifier to input data

    predict(x)
        Uses the classifier to make predictions on new input

    score(x, y)
        Makes predctions for x and returns the accuracy of the classifier
        regarding the labels in y

    bootstrap_samples(x, y)
        Resamples input data (sampling with replacement)
        For simplicity, output has the same amount of samples as the input.

    """

    def __init__(self, max_depth, n_estimators):
        self.max_depth = max_depth
        self.n_estimators = n_estimators

    def fit(self, x, y):
        """ Fits classifier to bootstraped input data

        Parameters:
        -----------
        x : array_like
            predictors
        y : array_like
            labels
        """
        # TODO:

    def predict(self, x):
        """ Uses the classifier to make predictions on new input data

        Parameters:
        -----------
        x : array_like
            predictors
        """
        # TODO:

    def score(self, x, y):
        """ Makes predctions for x and returns the accuracy of the classifier
        regarding the labels in y

        Parameters:
        -----------
        x : array_like
            predictors
        y : array_like
            labels

        Returns:
        --------
        float : accuracy of prediction
        """
        # TODO:

    def bootstrap_samples(self, x, y):
        """ Resamples input data (sampling with replacement)
        For simplicity, output has the same amount of samples as the input.

        Parameters:
        -----------
        x : array_like
            predictors
        y : array_like
            labels

        Returns:
        --------
        array_like, array_like : sampled x and y
        """
        # TODO:
