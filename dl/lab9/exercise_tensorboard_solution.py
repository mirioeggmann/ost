#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:44:44 2021

@author: simon
"""

import tensorflow as tf

from tensorflow.keras.layers import Dense, Softmax
from tensorflow.keras import Model

import numpy as np

###############################################################################
#
# Load and prepare data
#
###############################################################################

# Load 
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_valid, y_valid) = mnist.load_data()

# Scale images
x_train = x_train / 255.0
x_valid = x_valid / 255.0

# Flatten images
x_train = x_train.reshape([len(x_train), -1]).astype("float32")
x_valid = x_valid.reshape([len(x_valid), -1]).astype("float32")

# Convert labels to one-hot tensor
y_train = tf.one_hot(y_train, 10)
y_valid = tf.one_hot(y_valid, 10)

# Create Datasets 
MINI_BATCH_SIZE = 32
train_ds = tf.data.Dataset.from_tensor_slices(
           (x_train, y_train)).shuffle(10000).batch(MINI_BATCH_SIZE)
valid_ds = tf.data.Dataset.from_tensor_slices(
           (x_valid, y_valid)).batch(MINI_BATCH_SIZE)

###############################################################################
#
# Create model, define optimizer,  loss and metrics
#
###############################################################################

class MyModel(Model):
    def __init__(self, name=None, **kwargs):
        super(MyModel, self).__init__(name=name, **kwargs)
        self.d1 = Dense(10, use_bias=True, name='Dense_1')
        self.s1 = Softmax(name='Softmax_1')
        
    @tf.function
    def call(self, x, training=False):
        x   = self.d1(x)
        out = self.s1(x)
        return out

# Create an instance of the model
model = MyModel(name='MNISTClassifier')

# Choose an optimizer and loss function for training:
loss_object = tf.keras.losses.CategoricalCrossentropy()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

# Select metrics to measure the loss and the accuracy of the model.
# These metrics accumulate the values over epochs and then print the overall result.
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.CategoricalAccuracy(name='train_accuracy')

valid_loss = tf.keras.metrics.Mean(name='valid_loss')
valid_accuracy = tf.keras.metrics.CategoricalAccuracy(name='valid_accuracy')

###############################################################################
#
# Define train step and valid step
#
###############################################################################

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
    
    mislabeled = tf.not_equal(tf.argmax(predictions, axis=1),
                              tf.argmax(labels, axis=1))
    mislabled_imgs = tf.boolean_mask(images, mislabeled)
    
    return mislabled_imgs

###############################################################################
#
# Prepare tensorboard stuff
#
###############################################################################

train_log_dir = 'logs/1_run/train'
test_log_dir  = 'logs/1_run/test'
func_log_dir  = 'logs/1_run/func'
hist_log_dir  = 'logs/1_run/hist'
image_log_dir = 'logs/1_run/image'

train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer  = tf.summary.create_file_writer(test_log_dir)
graph_writer         = tf.summary.create_file_writer(func_log_dir)
hist_writer          = tf.summary.create_file_writer(hist_log_dir)
image_writer         = tf.summary.create_file_writer(image_log_dir)

# Graph
tf.summary.trace_on(graph=True)

# Call only one tf.function when tracing.
dummy_batch = next(train_ds.as_numpy_iterator())
model(dummy_batch[0])

with graph_writer.as_default():
    tf.summary.trace_export(name="MNISTClassifier",
                            step=0)
tf.summary.trace_off()

###############################################################################
#
# Run training
#
###############################################################################

EPOCHS = 25
for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    valid_loss.reset_states()
    valid_accuracy.reset_states()
    
    # Train
    for images, labels in train_ds:
        train_step(images, labels)
    
    # Validate
    img_list = []
    for valid_images, valid_labels in valid_ds:
        mislabled_imgs = valid_step(valid_images, valid_labels)
        img_list.append(mislabled_imgs)

    # Scalars
    with train_summary_writer.as_default():
        tf.summary.scalar('loss',     train_loss.result(),     step=epoch)
        tf.summary.scalar('accuracy', train_accuracy.result(), step=epoch)
    with test_summary_writer.as_default():
        tf.summary.scalar('loss',     valid_loss.result(),     step=epoch)
        tf.summary.scalar('accuracy', valid_accuracy.result(), step=epoch)
    
    # Histogram
    with hist_writer.as_default():
        tf.summary.histogram('Weights', model.trainable_weights[0], step=epoch)
        tf.summary.histogram('Bias',    model.trainable_weights[1], step=epoch)
        
    # Images
    with image_writer.as_default():
        img_arr = tf.concat(img_list, axis=0)
        image = tf.concat((tf.reshape(img_arr[0:3,:], (-1,84,28,1)),
                           tf.reshape(img_arr[3:6,:], (-1,84,28,1)),
                           tf.reshape(img_arr[6:9,:], (-1,84,28,1)),
                           tf.reshape(img_arr[9:12,:], (-1,84,28,1))), axis=2)
        tf.summary.image('Incorrectly classified', image, step=epoch, max_outputs=1,)
    
    print(
      'Epoch {:2d}, '.format(epoch+1),
      'Loss: {:3.3f}, '.format(train_loss.result()),
      'Accuracy: {:3.3f}%, '.format(train_accuracy.result() * 100),
      'Valid Loss: {:3.3f}, '.format(valid_loss.result()),
      'Valid Accuracy: {:3.3f}%'.format(valid_accuracy.result() * 100)
    )