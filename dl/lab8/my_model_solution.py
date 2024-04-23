import tensorflow as tf


class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = tf.keras.layers.Dense(100, use_bias=True)
        self.r1 = tf.keras.layers.ReLU()
        self.d2 = tf.keras.layers.Dense(10, use_bias=True)
        self.s1 = tf.keras.layers.Softmax()

    def call(self, x):
        x = self.d1(x)
        x = self.r1(x)
        x = self.d2(x)
        return self.s1(x)
