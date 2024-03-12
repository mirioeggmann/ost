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
        pass

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
        predictions = None
        return predictions
