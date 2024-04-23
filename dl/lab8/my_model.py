import tensorflow as tf


class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = tf.keras.layers.Dense(10, use_bias=True)
        self.s1 = tf.keras.layers.Softmax()

    def call(self, x):
        x = self.d1(x)
        return self.s1(x)
