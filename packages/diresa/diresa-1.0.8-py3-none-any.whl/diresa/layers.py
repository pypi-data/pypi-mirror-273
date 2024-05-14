#!/usr/bin/env python3
"""
DIRESA custom layer classes
:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import keras
import tensorflow as tf
from keras import layers


class Sampling(layers.Layer):
    """
        Samples from distribution with z_mean and z_log_var
        https://keras.io/examples/generative/vae/
    """

    def __init__(self, name=None, **kwargs):
        super(Sampling, self).__init__(name=name, **kwargs)

    def call(self, inputs):
        """
        :param inputs: [mean values, log of variances] of encoder model, shape=(2, batch_size, latent_size)
        :return: sample from the distribution
        """
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    def get_config(self):
        cfg = super().get_config()
        return cfg


class DistLayer(keras.layers.Layer):
    """
    Calculates distances between the 2 inputs and distances between the 2 latent representations of a twin model
    """

    def __init__(self, dim_less=False, name=None, **kwargs):
        """
        :param dim_less: if True distance is divided by dimension of space
        """
        super(DistLayer, self).__init__(name=name, **kwargs)
        self.dim_less = dim_less

    def call(self, x1, x2, y1, y2):
        """
        :param x1: batch of input samples to encoder
        :param x2: batch of input shuffled samples to twin encoder
        :param y1: batch of latent representations of encoder
        :param y2: batch of latent representations of twin encoder
        :return: batch of distances between inputs, batch of distances between latent representations
        """
        dist1 = tf.math.reduce_sum(tf.math.square(x1 - x2), axis=range(1, tf.rank(x1)))  # sum over all dims, except 0
        dist2 = tf.math.reduce_sum(tf.math.square(y1 - y2), axis=range(1, tf.rank(y1)))  # sum over all dims, except 0
        if self.dim_less:
            dist1 /= tf.math.reduce_sum(x1) / x1.shape[1]  # divide by input dimension
            dist2 /= tf.math.reduce_sum(x2) / x2.shape[1]  # divide by latent space dimension
        return tf.stack((dist1, dist2), axis=-1)

    def get_config(self):
        cfg = super().get_config()
        return cfg


class MaskLayer(keras.layers.Layer):
    """
        MaskLayer as in Royen et al. (2021) - MaskLayer: Enabling scalable deep learning solutions by training embedded feature sets
    """

    def __init__(self, inference_units=0, name=None, **kwargs):
        """
        :param inference_units: number of units from latent space to be used during inference
        """
        super(MaskLayer, self).__init__(name=name, **kwargs)
        self.units = None
        self.inference_units = inference_units

    def build(self, input_shape):
        """
        :param input_shape: latent shape
        """
        self.units = input_shape[-1]

    def call(self, inputs, training):
        """
        :param inputs: layer inputs
        :param training: True during training, False during inference
        :return: inference: masked latent batch, training: random masked latent batch (scaled)
        """
        if training:
            size = tf.experimental.numpy.random.randint(self.units) + 1
            mask = tf.concat(
                [tf.ones([size], dtype="float32"),
                 tf.zeros([self.units - size], dtype="float32")], 0)
            outputs = tf.multiply(inputs, mask)
            outputs = tf.scalar_mul(tf.cast(self.units / size, dtype="float32"), outputs)
        else:
            if self.inference_units != 0:
                mask = tf.concat(
                    [tf.ones([self.inference_units], dtype="float32"),
                     tf.zeros([self.units - self.inference_units], dtype="float32")], 0)
                outputs = tf.multiply(inputs, mask)
        return outputs

    def get_config(self):
        cfg = super().get_config()
        return cfg
