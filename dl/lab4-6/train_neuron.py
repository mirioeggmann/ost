"""Script that trains and evaluates a single neuron."""

import numpy as np

from dataset import read_datasets
from plotting import plot_results
import neuron


def train_neuron(
    data_path: str,
    linearly_separable: bool,
    batch_size: int,
    learning_rate: float,
    n_epochs: int,
):
    """Load datasets and train and test the neural network.

    Args:
        data_path: path where the .mat files are stored
        linearly_separable: if True, linear separable dataset is loaded
                            if False, linear non-separable dataset is loaded
        batch_size: number of examples in a mini-batch
        learning_rate: the learning rate to use in gradient descend
        n_epochs: the number of epochs to train the neuron for
    """

    # Load datasets
    datasets = read_datasets(data_path, linearly_separable)
    n_inputs = datasets.train.n_inputs
    n_outputs = datasets.train.n_outputs
    assert n_inputs == 2
    assert n_outputs == 1

    # Initialize weights and bias
    w = np.random.normal(0, 0.58, (n_inputs))
    b = np.zeros(n_outputs)

    # Train neuron
    epoch = 0
    while epoch < n_epochs:
        # Get training data of next mini-batch
        batch_inputs, batch_labels = datasets.train.get_next_batch(batch_size)

        # Update weights and bias
        w, b = neuron.update_weights(batch_inputs, batch_labels, w, b, learning_rate)

        if datasets.train.is_epoch_completed(batch_size):
            # Epoch completed: calculate current loss of validation set
            epoch += 1
            validation_inputs, validation_labels = datasets.validation.get_next_batch()
            loss = neuron.loss_function(validation_inputs, validation_labels, w, b)
            print("epoch: {0:6d}    loss: {1:.8f}".format(epoch, loss))

    # Evaluate trained neuron
    test_inputs, test_labels = datasets.test.get_next_batch()
    predicted_labels, performance = neuron.evaluate_prediction(
        test_inputs, test_labels, w, b
    )
    print("\nPerformance on test set: {0:.2f} %".format(performance))
    plot_results(test_inputs, test_labels, predicted_labels)


if __name__ == "__main__":

    train_neuron(
        data_path="./data",
        linearly_separable=True,
        batch_size=500,
        learning_rate=0.5,
        n_epochs=1000,
    )
