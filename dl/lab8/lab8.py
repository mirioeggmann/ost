import tensorflow as tf
from keras.layers import Dense, Softmax, ReLU
from keras import Model
import numpy as np

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

x_train = x_train.reshape([len(x_train), -1]).astype("float32")
x_test = x_test.reshape([len(x_test), -1]).astype("float32")

indices = np.random.choice(len(y_train), 5000)
x_valid = x_train[indices, :]
y_valid = y_train[indices]

x_train = np.delete(x_train, np.where(indices)[0], axis=0)
y_train = np.delete(y_train, np.where(indices)[0], axis=0)

y_train = tf.one_hot(y_train, 10)
y_test = tf.one_hot(y_test, 10)
y_valid = tf.one_hot(y_valid, 10)

MINI_BATCH_SIZE = 32
train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).shuffle(10000).batch(MINI_BATCH_SIZE)
valid_ds = tf.data.Dataset.from_tensor_slices(
    (x_valid, y_valid)).batch(MINI_BATCH_SIZE)
test_ds = tf.data.Dataset.from_tensor_slices(
    (x_test, y_test)).batch(MINI_BATCH_SIZE)


class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = Dense(100, use_bias=True)
        self.r1 = ReLU()
        self.d2 = Dense(10, use_bias=True)
        self.s1 = Softmax()


    def call(self, x):
        x = self.d1(x)
        x = self.r1(x)
        x = self.d2(x)
        out = self.s1(x)
        return out


model = MyModel()

loss_object = tf.keras.losses.CategoricalCrossentropy()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.CategoricalAccuracy(name='train_accuracy')

valid_loss = tf.keras.metrics.Mean(name='valid_loss')
valid_accuracy = tf.keras.metrics.CategoricalAccuracy(name='valid_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.CategoricalAccuracy(name='test_accuracy')

@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)

@tf.function
def valid_step(images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    valid_loss(t_loss)
    valid_accuracy(labels, predictions)

@tf.function
def test_step(images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)

EPOCHS = 25

for epoch in range(EPOCHS):
    train_loss.reset_states()
    train_accuracy.reset_states()
    valid_loss.reset_states()
    valid_accuracy.reset_states()

    for images, labels in train_ds:
        train_step(images, labels)
    for images, labels in valid_ds:
        valid_step(images, labels)

    print(
        f'Epoch {epoch + 1}, '
        f'Loss: {train_loss.result()}, '
        f'Accuracy: {train_accuracy.result() * 100}, '
        f'Valid Loss: {valid_loss.result()}, '
        f'Valid Accuracy: {valid_accuracy.result() * 100}'
    )

test_loss.reset_states()
test_accuracy.reset_states()
for images, labels in test_ds:
    test_step(images, labels)

print(
    f'Test Loss: {test_loss.result()}, '
    f'Test Accuracy: {test_accuracy.result() * 100}'
)


