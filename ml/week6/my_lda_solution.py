"""
SOLUTION

29.10.2019 / Sascha Jecklin
23.09.2020 / Simon Walser

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
        self.predictors = x.shape[1]                               # number of features
        self.class_labels = np.unique(y)                           # labels of classes
        self.classes = self.class_labels.shape[0]                  # number of classes
        self.pi = np.zeros(self.classes)                           # init for prior probbability vec
        self.sigma = np.zeros((self.predictors, self.predictors))  # sigma init
        self.mu = np.zeros((self.classes, self.predictors))        # mu init
        for i in range(self.classes):                              # calc pi, mu and sigma for all classes
            sub_x = x[y == self.class_labels[i]]
            self.pi[i] = len(sub_x)/len(y)
            self.mu[i,:] = np.mean(sub_x, axis=0)
            self.sigma += np.cov(sub_x, rowvar=False, ddof=(len(sub_x)-1))
            # cov = 1 / (N -ddfof) * sum((x - mu)**2)

        self.sigma /= (len(x) - self.classes)
        self.inv_sigma = np.linalg.inv(self.sigma)                 # inverse of sigma
        return self.mu

    def predict(self, x):
        """ Predicts class of input vectors

        Parameters:
        x : array_like
            input vectors

        Return:
        array_like : predictions
        """

        delta = np.empty([len(x), self.classes])

        # Iterate over all classes
        for i in range(self.classes):
            # equation 4.19 from book
            delta_i = x @ self.inv_sigma @ self.mu[i, :].reshape([-1, 1]) \
                    - 0.5 * (self.mu[i, :].reshape([1, -1]) @ self.inv_sigma @ self.mu[i, :].reshape([-1, 1])) \
                    + np.log(self.pi[i])
            delta[:, i] = np.squeeze(delta_i)

        predictions = self.class_labels[np.argmax(delta, axis=1)]

        return predictions

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
        predictions = self.predict(x)
        return sum(predictions == y)/len(y)


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

        # calc pi, mu and sigma for all classes
        for i in range(self.classes):                             
            sub_x = x[y == self.class_labels[i]]
            self.pi[i] = len(sub_x)/len(y)
            self.mu[i,:] = np.mean(sub_x, axis=0)
            self.sigma[i,:,:] = np.cov(sub_x, rowvar=False, ddof=1)
            # cov = 1 / (N -ddfof) * sum((x - mu)**2)
            self.inv_sigma[i,:,:] = np.linalg.inv(self.sigma[i,:,:]) # inverse of sigma
        return self.mu

    def predict(self, x):
        """ Predicts class of input vectors

        Parameters:
        x : array_like
            input vectors

        Return:
        array_like : predictions
        """

        delta = np.empty([len(x), self.classes])

        # Iterate over all classes
        for i in range(self.classes):
            # equation 4.19 from book
            delta_i = - 0.5 * np.sum(((x - self.mu[i,:]) @ self.inv_sigma[i, :, :]) * (x - self.mu[i,:]), axis=1) \
                      - 0.5 * np.log(np.linalg.det(self.sigma[i, :, :])) \
                      + np.log(self.pi[i])
            delta[:, i] = np.squeeze(delta_i)

        predictions = self.class_labels[np.argmax(delta, axis=1)]

        return predictions

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
        predictions = self.predict(x)
        return sum(predictions == y)/len(y)

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
