#!/usr/bin/env python3
"""
DIRESA helper functions

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

from keras.models import Model
from diresa.layers import MaskLayer, DistLayer, Sampling
from diresa.loss import (mae_dist_loss, male_dist_loss, mape_dist_loss, mse_dist_loss, msle_dist_loss,
                         corr_dist_loss, corr_log_dist_loss,
                         LatentCovLoss, KLLoss)


def cut_sub_model(model, sub_model_name):
    """
    Cuts a sub-model out of a keras model 
    Limitations: does not work for a sub-model of a sub-model
    
    :param model: keras model
    :param sub_model_name: name of the sub-model
    :return: submodel
    """
    sub_model_nbr = None
    sub_model_config = None

    custom_objects = {"MaskLayer": MaskLayer, "DistLayer": DistLayer, "Sampling": Sampling,
                      "KLLoss": KLLoss, "LatentCovLoss": LatentCovLoss, "mae_dist_loss": mae_dist_loss,
                      "male_log_dist_loss": male_dist_loss, "mape_log_dist_loss": mape_dist_loss,
                      "mse_dist_loss": mse_dist_loss, "msle_log_dist_loss": msle_dist_loss,
                      "corr_dist_loss": corr_dist_loss, "corr_log_dist_loss": corr_log_dist_loss,
                      }

    for nbr, layer in enumerate(model.get_config()['layers']):
        if layer['name'] == sub_model_name:
            sub_model_config = layer['config']
            sub_model_nbr = nbr

    if sub_model_config is None:
        print(sub_model_name, " not found in model")
        exit(1)

    sub_model = Model.from_config(sub_model_config, custom_objects=custom_objects)
    weights = [layer.get_weights() for layer in model.layers[sub_model_nbr].layers[1:]]

    for layer, weight in zip(sub_model.layers[1:], weights):
        layer.set_weights(weight)

    return sub_model
