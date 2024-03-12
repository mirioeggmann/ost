"""
Week7: own LDA implementation from scratch

29.10.2019 / Sascha Jecklin

"""

import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt


class LDA:
    def fit(self, x, y):
        """ LDA is a Liner Discriminant Model which can be fitted to data. It
        can then be used to make predictions for new samples.

        :param predictors: stores the number of predictors
        :param class_lables: stores the labels of all classes
        :param classes: stores the number of classes
        :param pi: stores the prior probbabilities pi
        :param sigma: stores the covariance matrix
        :param mu: stores the expected values
        :param inv_sigma: stores the inverse of sigma
        """
        self.predictors = x.shape[1] # number of features
        self.class_labels = np.unique(y) # labels of classes
        self.classes = self.class_labels.shape[0] # number of classes
        self.pi = np.zeros(self.classes) # init for prior probbability vec
        self.sigma = np.zeros((self.predictors, self.predictors))  # sigma init
        self.mu = np.zeros((self.classes, self.predictors))  # mu init
        # TODO calculate pi and mu for all classes

        # TODO calculate sigma

        # TODO calculate the inverse of sigma

        self.inv_sigma = 0
        return self.mu

    def predict(self, x):
        """ Predicts class of input vectors

        Parameters:
        x : array_like
            input vectors

        Return:
        array_like : predictions
        """
        return np.zeros(len(x))

    def score(self, x, y):
        """ Gives a measurment of correctly classified samples

        Parameters:
        x : array_like
            predictors
        y : array_like
            labels

        Returns:
        int : score
        """
        return 0.0




class QDA:
    def fit(self, x, y):
        """ QDA is a Quadratic Discriminant Model which can be fitted to data.
        It can then be used to make predictions for new samples.

        :param predictors: stores the number of predictors
        :param class_lables: stores the labels of all classes
        :param classes: stores the number of classes
        :param pi: stores the prior probbabilities pi
        :param sigma: stores the covariance matrix
        :param mu: stores the expected values
        :param inv_sigma: stores the inverse of sigma
        """
        self.predictors = x.shape[1] # number of features
        self.class_labels = np.unique(y) # labels of classes
        self.classes = self.class_labels.shape[0] # number of classes
        self.pi = np.zeros(self.classes) # init for prior probbability vec
        self.sigma = np.zeros((self.classes, self.predictors, self.predictors)) # sigma init
        self.inv_sigma = np.zeros((self.classes, self.predictors, self.predictors)) # sigma init
        self.mu = np.zeros((self.classes, self.predictors)) # mu init

        # TODO calculate pi and mu for all classes

        # TODO calculate sigma for all classes

        # TODO calculate the inverse of sigma for all classes

        self.inv_sigma = 0
        return self.mu

    def predict(self, x):
        """ Predicts class of input vectors

        Parameters:
        x : array_like
            input vectors

        Return:
        array_like : predictions
        """

        return np.zeros(len(x))

    def score(self, x, y):
        """ Gives a measurment of correctly classified samples

        Parameters:
        x : array_like
            predictors
        y : array_like
            labels

        Returns:
        int : score
        """

        return 0.0


if __name__ == '__main__':
    # Create artificial data set
    X, y = make_blobs(n_samples=200, centers=2, n_features=2, cluster_std=1.0, random_state=0)

    # Test fit
    lda = LDA()
    lda.fit(X, y)
    prediction = lda.predict(X)

    fig, axes = plt.subplots(1,1)
    axes.scatter(X[:,0], X[:,1], c=y, edgecolors=plt.get_cmap()(prediction*1000))
    plt.show()
