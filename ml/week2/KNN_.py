
import numpy as np

def KNN_(k, data, labels, t_data, t_labels=None):
    """
    KNN_: classifying using k-nearest neighbors algorithm. The nearest neighbors
    search method is euclidean distance
    Usage:
        predicted_labels, nn_index, accuracy = KNN_(3, training, training_labels, testing, testing_labels)
    Input:
        - k: number of nearest neighbors
        - data: (NxD) training data; N is the number of samples and D is the
        dimensionality of each data point
        - labels: training labels 
        - t_data: (MxD) testing data; M is the number of data points and D
        is the dimensionality of each data point
        - t_labels: testing labels (default = [])
    Output:
        - predicted_labels: the predicted labels based on the k-NN
        algorithm
        - nn_index: the index of the nearest training data point for each training sample (Mx1).
        - accuracy: if the testing labels are supported, the accuracy of
        the classification is returned, otherwise it will be zero.
    Author: Mahmoud Afifi - York University
    """

    # checks
    if t_labels is None:
        accuracy = 0

    assert data.shape[1] == t_data.shape[1], 'data should have the same dimensionality'


    #initialization
    predicted_labels = np.zeros((len(t_data),1))
    ed               = np.zeros((len(t_data),len(data))) #ed: (MxN) euclidean distances 
    ind              = np.zeros((len(t_data),len(data))) #corresponding indices (MxN)
    k_nn             = np.zeros((len(t_data),k))         #k-nearest neighbors for testing sample (Mxk)

    # TODO: Calculate euclidean distance between every training data sample and 
    # every test data sample and store result in the matrix ed.

    # TODO: For each test data sample sort the euclidian distances to every 
    # training data sample and store the indices of the corresponding training
    # data sample in the matrix ind.

    #find the nearest k for each data point of the testing data
    k_nn = ind[:, :k]
    nn_index = k_nn[:, 0]

    # get labels of nearest neighbours
    k_nn_label = labels[k_nn]
    options = np.unique(labels)

    #get the majority vote
    # TODO: Assign to each test data sample the training label which occures
    # most often in its neighbourhood. Store this label in the array predicted_labels

    #calculate the classification accuracy
    if t_labels is not None:
        accuracy = np.sum(predicted_labels == t_labels) / len(t_data)

    return predicted_labels, nn_index, accuracy
