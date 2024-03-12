#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:44:44 2021

@author: simon
"""

import tensorflow as tf
from tensorflow.keras.layers import Dense, Softmax
from tensorflow.keras import Model

# Load and prepare data
#############################################################################

# Load 
mnist = tf.keras.datasets.mnist
(x_train, y_train), _ = mnist.load_data()
# Scale images
x_train = x_train / 255.0
# Flatten images
x_train = x_train.reshape([len(x_train), -1]).astype("float32")
# Convert labels to one-hot tensor
y_train = tf.one_hot(y_train, 10)
# Create Datasets 
MINI_BATCH_SIZE = 32
train_ds = tf.data.Dataset.from_tensor_slices(
           (x_train, y_train)).shuffle(10000).batch(MINI_BATCH_SIZE)

# Create model, define optimizer, loss and metrics
#############################################################################

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
# Select metrics to measure the loss
train_loss = tf.keras.metrics.Mean(name='train_loss')

# Define train step
#############################################################################

# Use tf.GradientTape to train the model
@tf.function
def train_step(images, labels):
    # Collect gradients of trainable variables
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
        
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)

# Prepare TensorBoard
#############################################################################

scalar_log_dir = 'logs/1_run/scalar'
func_log_dir   = 'logs/1_run/func'
hist_log_dir   = 'logs/1_run/hist'
image_log_dir  = 'logs/1_run/image'

scalar_writer = tf.summary.create_file_writer(scalar_log_dir)
graph_writer  = tf.summary.create_file_writer(func_log_dir)
hist_writer   = tf.summary.create_file_writer(hist_log_dir)
image_writer  = tf.summary.create_file_writer(image_log_dir)

# Graph
tf.summary.trace_on(graph=True)

# Call only one tf.function when tracing
dummy_batch = next(train_ds.as_numpy_iterator())
model(dummy_batch[0])

with graph_writer.as_default():
    tf.summary.trace_export(name="MNISTClassifier", step=0)
tf.summary.trace_off()

# Run training
#############################################################################

EPOCHS = 25
for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    
    # Train
    for images, labels in train_ds:
        train_step(images, labels)
    
    # Write scalars to TensorBoard
    with scalar_writer.as_default():
        tf.summary.scalar('loss',     train_loss.result(),     step=epoch)
    
    # Write histogram to TensorBoard
    with hist_writer.as_default():
        tf.summary.histogram('Weights', model.trainable_weights[0], step=epoch)
        tf.summary.histogram('Bias',    model.trainable_weights[1], step=epoch)
        
    # Images
    with image_writer.as_default():
        image = tf.reshape(next(train_ds.as_numpy_iterator())[0][epoch,:], (1,28,28,1))
        tf.summary.image('Arbitrary image',
                         image,
                         step=epoch, max_outputs=1,)
    
    print(
      'Epoch {:2d}, '.format(epoch+1),
      'Loss: {:3.3f}, '.format(train_loss.result())
    )