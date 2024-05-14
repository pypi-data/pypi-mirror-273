#!/usr/bin/env python3
"""
DIRESA loss classes/functions

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import tensorflow as tf
import tensorflow_probability as tfp
from keras.losses import Loss


class KLLoss(Loss):
    """
    KL weighted loss class
    KL weight is annealed by KLAnnealingCallback
    """
    def __init__(self, kl_weight=1.):
        """
        :param kl_weight: tensorflow variable with initial KL loss weight
        """
        super().__init__()
        self.kl_weight = kl_weight

    def call(self, _, z_mean_var):
        """
        :param _: not used (loss functions need 2 params: the true and predicted values)
        :param z_mean_var: list with mean and ln of the variance of the distribution
        :return: weighted KL loss
        """
        z_mean, z_log_var = tf.split(z_mean_var, num_or_size_splits=2, axis=1)
        loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        return self.kl_weight * tf.reduce_mean(loss, axis=-1)


class LatentCovLoss(Loss):
    """
    Latent covariance loss class
    Latent covariance weight is annealed by AnnealingCallback
    """
    def __init__(self, cov_weight=1.):
        """
        :param cov_weight: tensorflow variable with initial covariance loss weight
        """
        super().__init__()
        self.cov_weight = cov_weight

    def call(self, _, latent):
        """
        :param _: not used (loss functions need 2 params: the true and predicted values)
        :param latent: batch of latent vectors
        :return: weighted covariance loss
        """
        cov = tf.math.abs(tfp.stats.covariance(latent))
        cov_square = tf.math.multiply(cov, cov)
        nbr_of_cov = tf.shape(latent)[-1] * (tf.shape(latent)[-1] - 1)
        cov_loss = (tf.math.reduce_sum(cov_square) - tf.linalg.trace(cov_square)) / tf.cast(nbr_of_cov, "float32")
        return self.cov_weight * cov_loss


def mae_dist_loss(_, distances):
    """
    Absolute Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute errors
    """
    ae = tf.math.abs(distances[:, 0] - distances[:, 1])
    return ae


def male_dist_loss(_, distances):
    """
    Absolute Error between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute logarithmic errors
    """
    ale = tf.math.abs(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return ale


def mape_dist_loss(_, distances):
    """
    Absolute Percentage Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute percentage errors
    """
    epsilon = 1e-8
    ape = tf.math.abs((distances[:, 0] - distances[:, 1]) / (distances[:, 0] + epsilon))
    return ape


def mse_dist_loss(_, distances):
    """
    Squared Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared errors
    """
    se = tf.math.square(distances[:, 0] - distances[:, 1])
    return se


def msle_dist_loss(_, distances):
    """
    Squared Error between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared logarithmic errors
    """
    sle = tf.math.square(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return sle


def corr_dist_loss(_, distances):
    """
    Correlation loss between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient
    """
    cov = tfp.stats.covariance(distances)
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


def corr_log_dist_loss(_, distances):
    """
    Correlation loss between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient (of logarithmic distances)
    """
    cov = tfp.stats.covariance(tf.math.log1p(distances))
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])
