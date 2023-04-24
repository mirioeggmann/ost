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
    return(x, y)

def main():

    # create training dataset
    x_train, y_train = noisy_data()
    
    # visualize the data as scatter plot
    fig1 = plt.figure(1)
    plt.scatter(x_train, y_train)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


if __name__ == '__main__':
    main()
