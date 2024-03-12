import numpy as np
from scipy.spatial import distance

class MyKMeans():
    """ Implementation of K-Means clustering

    Parameters
    ----------
    int : n_cluster
          max depth of the threes

    Attributes
    ----------
    int : n_clusters
          The number of clusters to form as well as the number of centroids to
          generate.
    array_like : cluster_centers_
                 Coordinates of cluster centers.
    ...

    Methods
    -------
    fit(x, y)
        Compute k-means clustering

    predict(x)
        Predict the closest cluster each sample in x belongs to.
    """
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
        self.cluster_centers_ = 0

    def fit(self, x):
        """ Compute k-means clustering

        Parameters:
        -----------
        x : array_like
            data
        """
        n_features = x.shape[1]

        # initialize attrtibutes and variables
        self.cluster_centers_ = np.zeros((self.n_clusters, n_features))
        
        self.labels_ = np.random.choice(range(0, self.n_clusters), x.shape[0])
        labels_old_ = np.zeros(x.shape[0])

        for i in range(self.n_clusters):
            self.cluster_centers_[i, :] = np.mean(x[self.labels_ == i], axis=0)
        
        
        
        # calculate cluster centers until nothing changes
        while not (labels_old_ == self.labels_).all():
            distances = distance.cdist(x, self.cluster_centers_, 'euclidean')

            labels_old_ = self.labels_.copy()
            self.labels_ = np.argmin(distances, axis=1)  # take closest center

            # calculate new cluster center with new predictions
            for i in range(self.n_clusters):
                self.cluster_centers_[i, :] = np.mean(x[self.labels_ == i],
                                                      axis=0)
                                                      
        return self

    def predict(self, x):
        """ Predict the closest cluster each sample in x belongs to.

        Parameters:
        -----------
        x : array_like
            data

        Returns:
        --------
        predictions : array_like
                      closest cluster for each input sample
        """
        # get distances
        distances = distance.cdist(x, self.cluster_centers_, 'euclidean')

        # take cluster with shortest distance as prediciton
        predictions = np.argmin(distances, axis=1)
        return predictions
