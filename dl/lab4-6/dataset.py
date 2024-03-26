from dataclasses import dataclass
import os

import h5py
import numpy as np


class DataSet:
    """Class defining a single dataset consisting of inputs and labels."""

    def __init__(self, inputs, labels):
        """Initialize a new DataSet using the given inputs and corresponding
        labels.

        Args:
            inputs: numpy array with dimensions (n_samples, n_inputs)
            labels: numpy array with dimensions (n_samples, n_outputs)
        """

        assert inputs.shape[0] == labels.shape[0]

        self.n_samples = inputs.shape[0]
        self.n_inputs = inputs.shape[1]
        self.n_outputs = labels.shape[1]

        self._inputs = np.squeeze(inputs)
        self._labels = np.squeeze(labels)

        self.epochs_completed = 0
        self._index_in_epoch = 0

    def get_next_batch(self, batch_size=None):
        """Return the next 'batch_size' examples of the dataset.

        Args:
            batch_size: size of the batch

        Returns:
            data and labels of this dataset
        """

        if batch_size is None:
            batch_size = self.n_samples

        assert batch_size <= self.n_samples

        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self.n_samples:
            # Finished epoch
            self.epochs_completed += 1

            # Shuffle the data
            perm = np.arange(self.n_samples)
            np.random.shuffle(perm)
            self._inputs = self._inputs[perm]
            self._labels = self._labels[perm]

            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size

        end = self._index_in_epoch

        return self._inputs[start:end], self._labels[start:end]


@dataclass
class DataSets:
    """Class for grouping three 'DataSet' objects into a single object."""

    train: DataSet
    validation: DataSet
    test: DataSet


def read_datasets(path, linearly_separable=False):
    """Read the desired data form the mat-Files in `path` and store it in
    DataSet objects.

        Args:
            path:   directory where the data is stored
            linearly_separable: if True, linear separable dataset is loaded
                                if False, linear non-separable dataset is loaded

        Returns:
            dataSets object
    """

    VALIDATION_SIZE = 1000

    if linearly_separable:
        filepath = os.path.join(path, "linSepDataSet_2.mat")
    else:
        filepath = os.path.join(path, "linNonSepDataSet_2.mat")

    # Load data from mat-file
    mat_file = h5py.File(filepath, "r")
    inputs_train = np.transpose(np.array(mat_file.get("inputsTrain")))
    labels_train = np.transpose(np.array(mat_file.get("labelsTrain")))
    inputs_test = np.transpose(np.array(mat_file.get("inputsTest")))
    labels_test = np.transpose(np.array(mat_file.get("labelsTest")))
    mat_file.close()

    # Split off a validation set
    ind = np.arange(labels_train.shape[0])
    np.random.shuffle(ind)
    inputs_train = inputs_train[ind, :]
    labels_train = labels_train[ind, :]
    inputs_validation = inputs_train[:VALIDATION_SIZE, :]
    labels_validation = labels_train[:VALIDATION_SIZE, :]
    inputs_train = inputs_train[VALIDATION_SIZE:, :]
    labels_train = labels_train[VALIDATION_SIZE:, :]

    # Combine the three datasets
    datasets = DataSets(
        train=DataSet(inputs_train, labels_train),
        validation=DataSet(inputs_validation, labels_validation),
        test=DataSet(inputs_test, labels_test),
    )

    return datasets
