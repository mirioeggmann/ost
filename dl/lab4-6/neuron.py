"""Functions for training, evaluating and using a single neuron."""

import numpy as np


def evaluate_neuron(x, w, b):
    """Calculate the output of a neuron with two input nodes.
    The sigmoid function is used as activation function.

    Args:
        x: input (numpy array of size [batch_size, 2])
        w: weights (numpy array of size [2])
        b: bias (numpy array of size [1])

    Returns:
        y, a: output and pre-activation (numpy arrays of size [batch_size])
    """

    assert x.ndim == 2
    assert x.shape[1] == 2
    assert w.shape == (2,)
    assert b.shape == (1,) or b.shape == ()

    # TODO: add your code here

    return y, a


def derivative_of_sigmoid(a):
    """Calculate the derivative of the sigmoid function.

    Args:
        a: pre-activation of the neuron (numpy array of size [m, n])

    Returns:
        deriv: derivative (numpy array of size [m, n])
    """

    # TODO: add your code here

    return deriv


def loss_function(x, t, w, b):
    """Calculate the loss function of the neuron.

    Args:
        x: input (numpy array of size [batch_size, 2])
        t: target, desired output (numpy array of size [batch_size])
        w: weights (numpy array of size [2])
        b: bias (numpy array of size [1])

    Returns:
        loss: the calculated loss (scalar)
    """

    assert x.ndim == 2
    assert x.shape[1] == 2
    assert t.ndim == 1
    assert t.shape[0] == x.shape[0]
    assert w.shape == (2,)
    assert b.shape == (1,) or b.shape == ()

    # TODO: add your code here

    return loss


def update_weights(x, t, w, b, lr):
    """Update the weights and the bias by applying stochastic gradient descent.

    Args:
        x:  input (numpy array of size [batch_size, 2])
        t:  target, desired output (numpy array of size [batch_size])
        w:  weights (numpy array of size [2])
        b:  bias (numpy array of size [1])
        lr: learning rate

    Returns:
        w_new, b_new: updated weights and bias
    """

    assert x.ndim == 2
    assert x.shape[1] == 2
    assert t.ndim == 1
    assert t.shape[0] == x.shape[0]
    assert w.shape == (2,)
    assert b.shape == (1,) or b.shape == ()

    # TODO: add your code here

    return w_new, b_new


def evaluate_prediction(x, t, w, b):
    """Evaluate the prediction (predicted class) of the neuron.

    Args:
        x: input (numpy array of size [batch_size, 2])
        t: target, desired output (numpy array of size [batch_size])
        w: weights (numpy array of size [2])
        b: bias (numpy array of size [1])

    Returns:
        pred: predicted class (numpy array of size [batch_size])
        perf: performance in percent (amount of correct predictions)
    """

    assert x.ndim == 2
    assert x.shape[1] == 2
    assert t.ndim == 1
    assert t.shape[0] == x.shape[0]
    assert w.shape == (2,)
    assert b.shape == (1,) or b.shape == ()

    # TODO: add your code here

    return pred, perf


# Tests for the defined functions
if __name__ == "__main__":

    print("Start unit test for module neuron.py.")

    # test values
    x = np.array(
        [[1.56, 2.58], [-4.64, 2.43], [3.49, -1.08], [4.34, 1.55], [1.79, -3.29]]
    )
    w = np.array([2.06, -4.68])
    b = np.array(-2.23)
    t = np.array([1, 0, 0, 0, 1])
    y_target = np.array(
        [
            1.52517660984416e-05,
            8.73760411044216e-11,
            0.999955224291058,
            0.367350528619039,
            0.999999952121537,
        ]
    )
    a_target = np.array([-11.0908, -23.1608, 10.0138, -0.5436, 16.8546])
    loss_target = 0.213482635816409
    da = np.array(
        [
            1.52515334820725e-05,
            8.73760410967870e-11,
            4.47737040777816e-05,
            0.232404117742352,
            4.78784611854547e-08,
        ]
    )
    lr = 0.75
    w_new_target = np.array([2.00440180296548, -4.69983624753640])
    b_new_target = np.array([-2.24281049438565])
    pred_target = np.array([0, 0, 1, 0, 1])
    perf_target = 60

    # test function evaluate_neuron
    y_, a_ = evaluate_neuron(x, w, b)
    assert np.all(np.abs(a_target - a_) < 10e-15)
    assert np.all(np.abs(y_target - y_) < 10e-15)

    # test function derivative_of_sigmoid
    da_ = derivative_of_sigmoid(a_target)
    assert np.all(np.abs(da - da_) < 10e-15)

    # test function loss_function
    loss_ = loss_function(x, t, w, b)
    assert np.abs(loss_target - loss_) < 10e-15

    # test function update_wights
    w_new_, b_new_ = update_weights(x, t, w, b, lr)
    assert np.all(np.abs(w_new_target - w_new_) < 10e-15)
    assert np.all(np.abs(b_new_target - b_new_) < 10e-15)

    # test function predict
    pred_, perf_ = evaluate_prediction(x, t, w, b)
    assert np.all(np.abs(pred_target - pred_) < 10e-15)
    assert np.abs(perf_target - perf_) < 10e-15

    print("Unit test was successful.")
