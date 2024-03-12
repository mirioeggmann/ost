"""
SOLUTION

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
        self.models = []
        for i in range(self.n_estimators):
            # resampling the data
            x_sample, y_sample = self.bootstrap_samples(x, y.reshape(-1, 1))
            x_sample2, y_sample2 = self.bootstrap_samples(x, y.reshape(-1, 1))
            mdl = DecisionTreeClassifier(max_depth=self.max_depth)
            mdl.fit(x_sample, y_sample)
            self.models.append(mdl)
            
        return self

    def predict(self, x):
        """ Uses the classifier to make predictions on new input data

        Parameters:
        -----------
        x : array_like
            predictors
        """
        prediction = []
        for mdl in self.models:
            prediction.append(mdl.predict(x))
        prediction = np.array(prediction)
        # majority vote of different predictions
        prediction = np.round(np.sum(prediction, axis=0)/self.n_estimators)
        return prediction

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
        prediction = self.predict(x)
        return accuracy_score(y, prediction)

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
        # choose random indices which can then be used to mask x and y
        indices = np.random.choice(range(0, len(y)), len(y))
        return x[indices, :], y[indices]
