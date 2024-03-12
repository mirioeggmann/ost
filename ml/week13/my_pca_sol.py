import numpy as np


class MyPca():
    """ Implementation of Principal component analysis

    Parameters
    ----------
    int : n_components
          Number of components to keep. if n_components is not set all
          components are kept

    Attributes
    -----------
    float : mean
            Per-feature empirical mean, estimated from the training set.
    array_like : covariance
                 Covariance matrix of X
    array_like : eigen_vals
                 Eigen Values of the covariance matrix
    array_like : eigen_vecs
                 Eigen Vectors of the covariance matrix
    array_like : components_
                 Principal axes in feature space, representing the directions
                 of maximum variance in the data. The components are sorted
                 by explained_variance_.
    array_like : explained_variance_
                 The amount of variance explained by each of the selected
                 components.
    array_like : explained_variance_ratio_
                 Percentage of variance explained by each of the selected
                 components.

    Methods
    -------
    fit(x)
        Fit the model with X

    transform(x)
        Apply dimensionality reduction to X.

    inverse_transform(x)
        Transform data back to its original space.


    """
    def __init__(self, n_components=None):
        self.n_components = n_components
        self.mean = 0
        self.covariance = 0
        self.eigen_vals = 0
        self.eigen_vecs = 0
        self.components_ = 0
        self.explained_variance_ = 0
        self.explained_variance_ratio_ = 0

    def fit(self, x):
        self.n, self.m = x.shape

        # if no n_components is given use all component axis
        if self.n_components is None:
            self.n_components = self.m
        # there can't be more components then features
        assert self.n_components <= self.m

        # subtrac mean
        self.mean = np.mean(x, axis=0)
        x -= self.mean

        # compute covariance matrix
        self.covariance = x.T @ x / (self.n-1)

        # eigen-decomposition
        self.eigen_vals, self.eigen_vecs = np.linalg.eig(self.covariance)

        # sort after biggest eigen values
        idx = self.eigen_vals.argsort()[::-1]
        self.eigen_vals = self.eigen_vals[idx]
        self.eigen_vecs = self.eigen_vecs[:, idx]

        # components are eigen-vectors, explained variances are eigen-values
        self.components_ = self.eigen_vecs
        self.explained_variance_ = self.eigen_vals

        # proportion of variance explained (PVE) by each principal component
        total_var = np.var(x, ddof=1, axis=0).sum()
        # print("total var is *******:{}".format(total_var))
        self.explained_variance_ratio_ = self.explained_variance_ / total_var
        
        return self

    def transform(self, x):
        # dot product between x and components_
        x_pca = x @ self.components_[:, :self.n_components]
        return x_pca

    def inverse_transform(self, x):
        # dot product between x and transposed components
        # by taking a components with highest explained variance deminsionality
        # gets reduced
        return x @ self.components_.T[:self.n_components, :] + self.mean
