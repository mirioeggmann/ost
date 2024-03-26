import numpy as np
import matplotlib.pyplot as plt


def plot_results(inputs, true_labels, predicted_labels):
    """Plot results.

    Args:
        inputs: numpy array with dimensions (n_samples, n_inputs)
        true_labels: numpy array with dimensions (n_samples, n_outputs)
        predicted_labels: numpy array with dimensions (n_samples, n_outputs)
    """
    plt.figure()
    colors = ["b", "g", "m", "y"]
    legend = ["correct class 1", "correct class 2", "wrong class 1", "wrong class 2"]

    for label in range(2):
        ind = np.nonzero(
            np.all(
                np.array([true_labels == predicted_labels, true_labels == label]),
                axis=0,
            )
        )[0]
        if ind.size:
            plt.scatter(
                inputs[ind, 0],
                inputs[ind, 1],
                c=colors[label],
                marker="o",
                label=legend[label],
            )
        ind = np.nonzero(
            np.all(
                np.array([true_labels != predicted_labels, true_labels == label]),
                axis=0,
            )
        )[0]
        if ind.size:
            plt.scatter(
                inputs[ind, 0],
                inputs[ind, 1],
                c=colors[label + 2],
                marker="o",
                label=legend[label + 2],
            )

    plt.axis("equal")
    plt.grid()
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=4, fancybox=True)
    plt.show()
