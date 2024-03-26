#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:44:44 2021

@author: simon
"""

import tensorflow as tf
from keras.layers import Dense, Softmax, ReLU
from keras import Model

import numpy as np

# Load 
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Scale images
x_train = x_train / 255.0
x_test  = x_test / 255.0

# Flatten images
x_train = x_train.reshape([len(x_train), -1]).astype("float32")
x_test  = x_test.reshape([len(x_test), -1]).astype("float32")

# Create Validation dataset out of Training dataset
indices = np.random.choice(len(y_train), 5000)
x_valid = x_train[indices, :]
y_valid = y_train[indices]

x_train = np.delete(x_train, np.where(indices)[0], axis=0)
y_train = np.delete(y_train, np.where(indices)[0], axis=0)

# Convert labels to one-hot tensor
y_train = tf.one_hot(y_train, 10)
y_test  = tf.one_hot(y_test, 10)
y_valid  = tf.one_hot(y_valid, 10)

# Create Datasets 
MINI_BATCH_SIZE = 32
train_ds = tf.data.Dataset.from_tensor_slices(
           (x_train, y_train)).shuffle(10000).batch(MINI_BATCH_SIZE)
valid_ds = tf.data.Dataset.from_tensor_slices(
           (x_valid, y_valid)).batch(MINI_BATCH_SIZE)
test_ds  = tf.data.Dataset.from_tensor_slices(
           (x_test, y_test)).batch(MINI_BATCH_SIZE)

# Create model
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = Dense(100, use_bias=True)
        self.r1 = ReLU()
        self.d2 = Dense(10, use_bias=True)
        self.s1 = Softmax()

    def call(self, x):
        x   = self.d1(x)
        x   = self.r1(x)
        x   = self.d2(x)
        out = self.s1(x)
        return out

# Create an instance of the model
model = MyModel()

# Choose an optimizer and loss function for training:
loss_object = tf.keras.losses.CategoricalCrossentropy()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

# Select metrics to measure the loss and the accuracy of the model.
# These metrics accumulate the values over epochs and then print the overall result.
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.CategoricalAccuracy(name='train_accuracy')

valid_loss = tf.keras.metrics.Mean(name='valid_loss')
valid_accuracy = tf.keras.metrics.CategoricalAccuracy(name='valid_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.CategoricalAccuracy(name='test_accuracy')

# Use tf.GradientTape to train the model
@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        # training=True is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
        
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    
    train_loss(loss)
    train_accuracy(labels, predictions)
  
# Validate the model
@tf.function
def valid_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)
    
    valid_loss(t_loss)
    valid_accuracy(labels, predictions)
    
# Test the model
@tf.function
def test_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)
    
    test_loss(t_loss)
    test_accuracy(labels, predictions)


EPOCHS = 25
for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    valid_loss.reset_states()
    valid_accuracy.reset_states()
    
    for images, labels in train_ds:
        train_step(images, labels)
    
    for valid_images, valid_labels in valid_ds:
        valid_step(valid_images, valid_labels)
    
    print(
      'Epoch {:2d}, '.format(epoch+1),
      'Loss: {:3.3f}, '.format(train_loss.result()),
      'Accuracy: {:3.3f}%, '.format(train_accuracy.result() * 100),
      'Valid Loss: {:3.3f}, '.format(valid_loss.result()),
      'Valid Accuracy: {:3.3f}%'.format(valid_accuracy.result() * 100)
    )
    
# Test resulting classifier
test_loss.reset_states()
test_accuracy.reset_states()
for test_images, test_labels in test_ds:
    test_step(test_images, test_labels)

print(
  '\nTesting result: ',
  'Test Loss: {:3.3f}, '.format(test_loss.result()),
  'Test Accuracy: {:3.3f}%'.format(test_accuracy.result() * 100)
)