#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 19:49:27 2021

@author: simon
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# create a noisy classification dataset
def noisy_data(n=100):
    x = tf.random.uniform(shape=(n,))
    y = tf.convert_to_tensor(np.random.normal(x, 0.1) > 0.5, dtype=tf.float32)
    return x, y


def main():
    # create training dataset
    x_train, y_train = noisy_data()

    # visualize the data as scatter plot
    fig1 = plt.figure(1)
    plt.scatter(x_train, y_train)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    # declare trainable variables
    m = tf.Variable(0.)
    b = tf.Variable(0.)

    # prediction model
    @tf.function
    def pred_response(x):
        y = m * x + b
        return y

    # loss function
    binary_cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
    loss = binary_cross_entropy(y_true=y_train, y_pred=pred_response(x_train))
    print("Starting loss: ", loss.numpy())

    # gradient descent from scratch
    learning_rate = 0.05
    steps = 5000
    for i in range(steps):
        with tf.GradientTape() as tape:
            predictions = pred_response(x_train)
            loss = binary_cross_entropy(y_true=y_train, y_pred=predictions)

        # compute loss with respect to m and b
        gradients = tape.gradient(loss, [m, b])
        m.assign_sub(gradients[0] * learning_rate)
        b.assign_sub(gradients[1] * learning_rate)

        # track steps
        if i % 50 == 0:
            print("Step number: %d, has loss %f" % (i, loss.numpy()))
    print("\nGradient after %d steps: " % steps, gradients)

    # visualize result
    x_plot = np.linspace(0,1,100)
    y_plot = 1 / (1 + np.exp(-(x_plot * m.numpy() + b.numpy())))
    plt.figure(2)
    plt.scatter(x_train, y_train)
    plt.plot(x_plot, y_plot)
    plt.show()

if __name__ == '__main__':
    main()
