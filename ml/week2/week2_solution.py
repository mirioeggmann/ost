"""
Statistical Machine Learning - Chapter 3 - python

By N. Tobler
"""

import numpy as np
import matplotlib.pyplot as plt

def KNN(k, data, labels, t_data, t_labels=None):
    """
    KNN: classifying using k-nearest neighbors algorithm. The nearest neighbors
    search method is euclidean distance
    Usage:
        predicted_labels, nn_index, accuracy = KNN(3, training, training_labels, testing, testing_labels)
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

    # initialization
    predicted_labels = np.zeros((len(t_data), 1))
    ed = np.zeros((len(t_data), len(data))) #ed: (MxN) euclidean distances
    ind = np.zeros((len(t_data), len(data)), dtype=int) #corresponding indices (MxN)
    k_nn = np.zeros((len(t_data), k)) #k-nearest neighbors for testing sample (Mxk)

    # TODO: Calculate euclidean distance between every training data sample and
    # every test data sample and store result in the matrix ed.
    ed = np.linalg.norm(t_data[:, None] - data[None, :], axis=-1)

    # TODO: For each test data sample sort the euclidian distances to every
    # training data sample and store the indices of the corresponding training
    # data sample in the matrix ind.
    ind = np.argsort(ed, axis=1)

    # find the nearest k for each data point of the testing data
    k_nn = ind[:, :k]
    nn_index = k_nn[:, 0]

    # get labels of nearest neighbours
    k_nn_label = labels[k_nn]
    options = np.unique(labels)

    # get the majority vote
    # TODO: Assign to each test data sample the training label which occures
    # most often in its neighbourhood. Store this label in the array predicted_labels
    num_votes = np.sum(k_nn_label[None, :, :] == options[:, None, None], axis=-1)
    predicted_labels = options[np.argmax(num_votes, axis=0)]

    #calculate the classification accuracy
    if t_labels is not None:
        accuracy = np.sum(predicted_labels == t_labels) / len(t_data)

    return predicted_labels, nn_index, accuracy

def main():

    # Loading Data
    train_data = np.genfromtxt('./KNN_Train.csv', delimiter=',', skip_header=1)
    test_data  = np.genfromtxt('./KNN_Test.csv', delimiter=',', skip_header=1)

    X_train = train_data[:, :2]
    y_train = train_data[:, 2].astype(int)

    X_test = test_data[:, :2]
    y_test = test_data[:, 2].astype(int)

    # Call KNN function
    k = 3
    predicted_labels, nn_index, accuracy = KNN(k, X_train, y_train, X_test, y_test)

    print(f'Accuracy: {accuracy:1.4f}')

    plt.figure()
    plt.scatter(X_train[:, 0], X_train[:,1], 20, y_train)
    plt.scatter(X_test[:, 0], X_test[:, 1], 20, predicted_labels, edgecolors="red")
    plt.xlabel('1. Predictor')
    plt.ylabel('2. Predictor')
    plt.title('kNN classifier')
    plt.grid()

    ## Run KNN classifier with different k and display decision surface

    # Prepare predictor data for decision surface
    x1range = np.arange(np.min([X_train[:, 0], X_test[:, 0]]), np.max([X_train[:, 0], X_test[:, 0]]), 0.5)
    x2range = np.arange(np.min([X_train[:, 1], X_test[:, 1]]), np.max([X_train[:, 1], X_test[:, 1]]), 0.5)
    [xx1, xx2] = np.meshgrid(x1range,x2range)
    XGrid = np.stack((xx1.flatten(), xx2.flatten()), axis=-1)

    _, axs = plt.subplots(2, 2, tight_layout=True)
    axs = axs.flatten()
    for i in range(4):
        k = i * 4 + 1

        # Call KNN with different k
        predicted_labels_1, _, _ = KNN(k, X_train, y_train, X_test)
        predicted_labels_2, _, _ = KNN(k, X_train, y_train, XGrid)

        # Display decision surface
        axs[i].pcolor(xx1, xx2, np.reshape(predicted_labels_2, xx1.shape), alpha=0.2, shading='auto')

        # Display test samples
        axs[i].scatter(X_test[:,0], X_test[:,1], 20, predicted_labels_1)
        axs[i].set_title(f'kNN classifier k={k}')


    ## Plot error rate
    # TODO: Plot training error rate and test error rate as a function of
    # 1 / K (flexibility of KNN)

    k_arr = np.round(np.logspace(0, 2, 10)).astype(int)

    error_curve_test = np.zeros(k_arr.shape)
    error_curve_train = np.zeros(k_arr.shape)
    for i in range(len(k_arr)):
        # Find test error rate
        predicted_labels_test, _, _ = KNN(k_arr[i], X_train, y_train, X_test)
        error_test = np.sum(predicted_labels_test != y_test) / len(y_test)
        error_curve_test[i] = error_test

        # Find training error rate
        predicted_labels_train, _, _ = KNN(k_arr[i], X_train, y_train, X_train)
        error_train = np.sum(predicted_labels_train != y_train) / len(y_train)
        error_curve_train[i] = error_train

    plt.figure()
    plt.plot(1/k_arr, error_curve_test, label='Test Errors')
    plt.plot(1/k_arr, error_curve_train, label='Training Errors')
    plt.legend()
    plt.xlabel('1/K')
    plt.ylabel('Error Rate')

    # show all plots
    plt.show()

if __name__ == '__main__':
    main()
