"""Implementation of a tiny logistic regression model using TensorFlow."""

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def noisy_data(n=100):
    x = tf.random.uniform(shape=(n,))
    y = tf.convert_to_tensor(np.random.normal(x, 0.1) > 0.5, dtype=tf.float32)
    return x, y


# prediction model
class LogRegression:
    def __init__(self):
        # declare trainable variables
        self.m = tf.Variable(0.0)
        self.b = tf.Variable(0.0)

    @tf.function
    def __call__(self, x):
        print("tracing")
        return tf.add(tf.multiply(self.m, x), self.b)


def main():
    # create training dataset
    x_train, y_train = noisy_data()

    # loss function
    binary_cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

    # declare model
    log_reg_model = LogRegression()

    # compute loss prior to training
    y_pred = log_reg_model(x_train)
    loss = binary_cross_entropy(y_true=y_train, y_pred=y_pred)
    print(f"Loss prior to training: {loss.numpy():.6f}")

    # gradient descent from scratch
    learning_rate = 0.05
    steps = 5000

    for i in range(steps):
        with tf.GradientTape() as tape:
            y_pred = log_reg_model(x_train)
            loss = binary_cross_entropy(y_true=y_train, y_pred=y_pred)

        # compute gradient of loss with respect to m and b
        gradient = tape.gradient(loss, [log_reg_model.m, log_reg_model.b])

        # move a small step in the direction of the negative gradient
        log_reg_model.m.assign_sub(gradient[0] * learning_rate)
        log_reg_model.b.assign_sub(gradient[1] * learning_rate)

        # track steps
        if i % 1000 == 0:
            print(f"Step number {i}: loss = {loss.numpy():.6f}")

    print(f"\nGradient after {steps} steps:", gradient)



    # visualize the data as scatter plot
    x_plot = np.linspace(0, 1, 100)
    y_plot = 1 / (
            1 + np.exp(-(x_plot * log_reg_model.m.numpy() + log_reg_model.b.numpy()))
    )

    plt.scatter(x_train, y_train)
    plt.plot(x_plot, y_plot)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == "__main__":
    main()
