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

    ...

    Methods
    -------
    fit(x)
        Fit the model with X

    transform(x)
        Apply dimensionality reduction to X.

    inverse_transform(x)
        Transform data back to its original space.


    """
    # n_components needed for exercise 2
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
        # TODO: Implement the fit method
        pass

    def transform(self, x):
        # TODO: Implement the transform method
        pass

    def inverse_transform(self, x):
        # TODO: Implement the inverse_transform method. Needed in exercise two
        pass
