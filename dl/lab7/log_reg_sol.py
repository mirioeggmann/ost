""" Implementation of a tiny logistic regression model using TensorFlow.

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

# prediction model
class LogRegression():
    def __init__(self):
       # declare trainable variables
       self.m = tf.Variable(0.)
       self.b = tf.Variable(0.) 

    @tf.function
    def __call__(self, x):
        print('tracing')
        y = self.m * x + self.b
        return(y)
  
def main():

    # create training dataset
    x_train, y_train = noisy_data()
    
    # loss function
    binary_cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
    
    # declare model
    log_reg_model = LogRegression()
    
    # compute loss prior to training
    loss = binary_cross_entropy(y_true=y_train, y_pred=log_reg_model(x_train))
    print("Starting loss: ", loss.numpy())
    
    
    # gradient descent from scratch
    learning_rate = 0.05
    steps = 5000
    for i in range(steps):
        with tf.GradientTape() as tape:
            predictions = log_reg_model(x_train)
            loss = binary_cross_entropy(y_true=y_train, y_pred=predictions)
        
        # compute loss with respect to m and b
        gradients = tape.gradient(loss, [log_reg_model.m, log_reg_model.b])
        log_reg_model.m.assign_sub(gradients[0] * learning_rate)
        log_reg_model.b.assign_sub(gradients[1] * learning_rate)
        
        # track steps
        if i % 1000 == 0:
            print("Step number: %d, has loss %f" % (i, loss.numpy()))
    
    print("\nGradient after %d steps: " % steps, gradients)
    
    # visualize result
    x_plot = np.linspace(0,1,100)
    y_plot = 1 / (1 + np.exp(-(x_plot * log_reg_model.m.numpy() + log_reg_model.b.numpy())))
    plt.figure(2)
    plt.scatter(x_train, y_train)
    plt.plot(x_plot, y_plot)
    plt.show()


if __name__ == '__main__':
    main()
