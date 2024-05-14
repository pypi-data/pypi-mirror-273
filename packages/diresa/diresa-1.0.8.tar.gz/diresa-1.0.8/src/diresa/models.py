#!/usr/bin/env python3
"""
Creates DIRESA and (V)AE models out of an encoder and decoder model.
Creates DIRESA and AE models from hyperparameters.

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License

1. Creating (V)AE and Diresa models out of an encoder and decoder model:
  - autoencoder_model(x, encoder, decoder, mask_layer=False)
  - vae_model(x, encoder, decoder)
  - cov_reg_ae_model(x, encoder, decoder)
  - siamese_twin_model(x, x_twin, encoder, decoder)
  - diresa_model(x, x_twin, encoder, decoder)

2. Creating AE and Diresa models from hyperparameters
  - build_ae(input_shape, stack, stack_filters, latent_filters, kernel_size=(3, 3),
    conv_transpose=False, up_first=False, residual=False, batchnorm=False,
    dense_units=(), mask_layer=False,
    activation='relu', encoder_activation='linear', decoder_activation='linear')
  - build_diresa(input_shape, stack, stack_filters, latent_filters, kernel_size=(3, 3),
    conv_transpose=False, up_first=False, residual=False, batchnorm=False,
    dense_units=(),
    activation='relu', encoder_activation='linear', decoder_activation='linear')

   Encoder:
    - 0 or more [blocks] with C (Conv2D) or residual units and a P (MaxPooling layer)
    - 0 or 1 [block] of D (Dense layers)
    - optionally a mask layer (only for AE)
   Decoder:
    - 0 or 1 [block] with D (Dense layers)
    - 0 or more [blocks] with C (Conv2D) or residual units and an U (UpSampling layer)
   Examples:
    - stack;     dense_units;  Encoder;                Decoder (up_first=True);    Decoder (up_first=False)
    - [1];       ();           [C-P]-Cout;             [U-C]-Cout;                 [C-U]-Cout
    - [3];       ();           [C-C-C-P]-Cout;         [U-C-C-C]-Cout;             [C-U-C-C]-Cout
    - [1,1];     ();           [C-P]-[C-P]-Cout;       [U-C]-[U-C]-Cout;           [C-U]-[C-U]-Cout
    - ();        [20,10];      [D-Dout];               [D-Dout];                   [D-Dout]
    - [2];       [20,10];      [C-C-P]-[D-Dout];       [D-D]-[U-C]-Cout;           [D-D]-[C-U]-Cout
    - [1,1];     [20,10];      [C-P]-[C-P]-[D-Dout];   [D-D]-[U]-[U-C]-Cout;       [D-D]-[U]-[C-U]-Cout

   If conv_transpose=True, C is a ConvTranspose layer, only possible for up_first=True.
   If residual=True, C is a residual unit with a skip connection, only possible for up_first=True.
   Input shape should be 3 if Conv2D blocks, first 2 dimensions of input_shape should be a multiple of 2^len(stack).
   Input shape should be 1 if only a Dense block.
"""


import tensorflow as tf
from math import prod as _prod
from keras import layers, Input
from keras.models import Model
from diresa.layers import DistLayer, MaskLayer


def autoencoder_model(x, encoder, decoder, mask_layer=False):
    """
    Creates autoencoder model out of an encoder and a decoder model
    
    :param x: keras input tensor (keras.Input())
    :param encoder: encoder functional Keras model
    :param decoder: decoder functional Keras model
    :param mask_layer: if True, adds a MaskLayer to the encoder
    :return: autoencoder model
    """
    y = encoder(x)

    if mask_layer:
        enc_output_shape = y.shape
        # if encoder output is not flat
        if len(enc_output_shape) != 2:
            y = layers.Flatten()(y)
        y = MaskLayer(name='MaskLayer')(y)
        # if encoder output is not flat
        if len(enc_output_shape) != 2:
            y = layers.Reshape(enc_output_shape[1:])(y)

    y = decoder(y)
    return Model(x, y)


def cov_reg_ae_model(x, encoder, decoder):
    """
    Creates a covariance regulated autoencoder model out of an encoder and a decoder model
    
    :param x: keras input tensor (keras.Input())
    :param encoder: encoder functional Keras model
    :param decoder: decoder functional Keras model
    :return: covariance regulated autoencoder model
    """
    encoded = encoder(x)
    latent = layers.Flatten(name="Latent")(encoded)
    y = decoder(latent)
    return Model(x, (y, latent))


def siamese_twin_model(x, x_twin, encoder, decoder, dist_layer=DistLayer()):
    """
    Creates a Diresa model (without cov regularization on latent space) out of an encoder and a decoder model
    
    :param x: keras input tensor (keras.Input())
    :param x_twin: keras input tensor for shuffled input
    :param encoder: encoder functional Keras model
    :param decoder: decoder functional Keras model
    :param dist_layer: distance layer to be used
    :return: Diresa model without cov regularization on latent space
    """
    latent = encoder(x)
    latent_twin = encoder(x_twin)
    dist = dist_layer(x, x_twin, latent, latent_twin)
    output = decoder(latent)
    return Model((x, x_twin), (output, dist))


def diresa_model(x, x_twin, encoder, decoder, dist_layer=DistLayer()):
    """
    Creates a Diresa model out of an encoder and a decoder model
    
    :param x: keras input tensor (keras.Input())
    :param x_twin: keras input tensor for shuffled input
    :param encoder: encoder functional Keras model
    :param decoder: decoder functional Keras model
    :param dist_layer: distance layer to be used
    :return: Diresa model
    """
    latent_orig = encoder(x)
    latent_twin = encoder(x_twin)
    dist = dist_layer(x, x_twin, latent_orig, latent_twin)
    latent = layers.Flatten(name="Latent")(latent_orig)
    output = decoder(latent_orig)
    return Model((x, x_twin), (output, latent, dist))


def vae_model(x, encoder, decoder):
    """
    Creates a variational autoencoder model out of an encoder and a decoder model
    
    :param x: keras input tensor (keras.Input())
    :param encoder: variational encoder functional Keras model
    :param decoder: decoder functional Keras model
    :return: variational autoencoder model
    """
    z, z_mean, z_log_var = encoder(x)
    y = decoder(z)
    return Model(x, (y, [z_mean, z_log_var]))


def build_ae(input_shape=(),
             stack=(),
             stack_filters=(),
             latent_filters=1,
             kernel_size=(3, 3),
             conv_transpose=False,
             up_first=False,
             residual=False,
             batchnorm=False,
             dense_units=(),
             mask_layer=False,
             activation='relu',
             encoder_activation='linear',
             decoder_activation='linear',
             ):
    """
    Creates an AE model out of hyperparameters
    
    :param input_shape: 3-dimensional with Conv2D layers, first 2 dimensions should be a multiple of 2^len(stack), 
        1-dimensional if only Dense layers
    :param stack: elements are nbr of Conv2D or residual units in a block
    :param stack_filters: elements are nbr of filters in a block
    :param latent_filters: nbr of filters in convolutional output (only used if no dense units)
    :param kernel_size: kernel size for convolution
    :param conv_transpose: if True ConvTranspose is used in decoder, only possible for up_first=True
    :param up_first: if True UpSampling is first in decoder block, if False UpSampling is second
    :param residual: if True, elements in blocks are residual units, if False elements are Conv2D layers
    :param batchnorm: if True, each Conv2D is followed by a BatchNormalization layer, if False no BN is used
    :param dense_units: elements are nbr of nodes of a Dense layer in the dense block
    :param mask_layer: if True a MaskLayer is added between encoder and decoder
    :param activation: activation function used (except for output of encoder/decoder)
    :param encoder_activation: activation function used for output of encoder
    :param decoder_activation: activation function used for output of decoder
    :return: AE functional Keras model
    """

    encoder = _encoder_model(input_shape=input_shape,
                             stack=stack,
                             stack_filters=stack_filters,
                             latent_filters=latent_filters,
                             kernel_size=kernel_size,
                             conv_transpose=conv_transpose,
                             up_first=up_first,
                             residual=residual,
                             batchnorm=batchnorm,
                             dense_units=dense_units,
                             activation=activation,
                             encoder_activation=encoder_activation,
                             )
    decoder = _decoder_model(input_shape=input_shape,
                             stack=stack,
                             stack_filters=stack_filters,
                             latent_filters=latent_filters,
                             kernel_size=kernel_size,
                             conv_transpose=conv_transpose,
                             up_first=up_first,
                             residual=residual,
                             batchnorm=batchnorm,
                             dense_units=dense_units,
                             activation=activation,
                             decoder_activation=decoder_activation,
                             )

    x = Input(shape=input_shape)

    return autoencoder_model(x, encoder, decoder, mask_layer)


def build_diresa(input_shape=(),
                 stack=(),
                 stack_filters=(),
                 latent_filters=1,
                 kernel_size=(3, 3),
                 conv_transpose=False,
                 up_first=False,
                 residual=False,
                 batchnorm=False,
                 dense_units=(),
                 activation='relu',
                 encoder_activation='linear',
                 decoder_activation='linear',
                 dist_layer=DistLayer(),
                 ):
    """
    Creates a Diresa model out of hyperparameters
    
    :param input_shape: 3-dimensional with Conv2D layers, first 2 dimensions should be a multiple of 2^len(stack)
        1-dimensional if only Dense layers
    :param stack: elements are nbr of Conv2D or residual units in a block
    :param stack_filters: elements are nbr of filters in a block
    :param latent_filters: nbr of filters in convolutional output (only used if no dense units)
    :param kernel_size: kernel size for convolution
    :param conv_transpose: if True ConvTranspose is used in decoder, only possible for up_first=True
    :param up_first: if True UpSampling is first in decoder block, if False UpSampling is second
    :param residual: if True, elements in blocks are residual units, if False elements are Conv2D layers
    :param batchnorm: if True, each Conv2D is followed by a BatchNormalization layer, if False no BN is used
    :param dense_units: elements are nbr of nodes of a Dense layer in the dense block
    :param activation: activation function used (except for output of encoder/decoder)
    :param encoder_activation: activation function used for output of encoder
    :param decoder_activation: activation function used for output of decoder
    :param dist_layer: distance layer to be used
    :return: Diresa functional Keras model
    """

    encoder = _encoder_model(input_shape=input_shape,
                             stack=stack,
                             stack_filters=stack_filters,
                             latent_filters=latent_filters,
                             kernel_size=kernel_size,
                             conv_transpose=conv_transpose,
                             up_first=up_first,
                             residual=residual,
                             batchnorm=batchnorm,
                             dense_units=dense_units,
                             activation=activation,
                             encoder_activation=encoder_activation,
                             )
    decoder = _decoder_model(input_shape=input_shape,
                             stack=stack,
                             stack_filters=stack_filters,
                             latent_filters=latent_filters,
                             kernel_size=kernel_size,
                             conv_transpose=conv_transpose,
                             up_first=up_first,
                             residual=residual,
                             batchnorm=batchnorm,
                             dense_units=dense_units,
                             activation=activation,
                             decoder_activation=decoder_activation,
                             )

    input_orig = Input(name="Input", shape=input_shape)
    input_twin = Input(name="Shuffled_Input", shape=input_shape)

    return diresa_model(input_orig, input_twin, encoder, decoder, dist_layer=dist_layer)


#
# Helper functions for creating the encoder and decoder models out of the hyperparameters
#
def _residual_unit(x, filters, kernel_size, activation, name):
    y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                      name=name + '_A')(x)
    y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                      name=name + '_B')(y)
    # If input has a  different nbr of filters
    if x.shape[-1] != filters:
        x = layers.Conv2D(filters, (1, 1), activation=activation, padding='same',
                          name=name + '_C')(x)
    return layers.Add(name=name.replace("Conv2D", "Add"))([x, y])


def _encoder_block(y, block, filters, kernel_size, residual, batchnorm, activation, name):
    # Block of num residual or Conv2D units followed by a MaxPooling2D layer
    for unit in range(block):
        if residual:
            y = _residual_unit(y, filters, kernel_size, activation=activation,
                               name=name + "_Conv2D_" + str(unit))
        else:
            y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                              name=name + "_Conv2D_" + str(unit))(y)
        if batchnorm:
            y = layers.BatchNormalization()(y)
    y = layers.MaxPooling2D((2, 2), padding='same', name=name + '_MaxPooling2D')(y)
    return y


def _decoder_block(y, block, filters, kernel_size, conv_transpose, residual, batchnorm, activation, up_first, name):
    if up_first:
        # Block of an UpSampling2D layer followed by num residual or Conv2D units
        y = layers.UpSampling2D((2, 2), name=name + '_UpSampling2D')(y)
        for unit in range(block):
            if residual:
                y = _residual_unit(y, filters, kernel_size, activation=activation,
                                   name=name + "_Conv2D_" + str(unit))
            elif conv_transpose:
                y = layers.Conv2DTranspose(filters, kernel_size, activation=activation, padding='same',
                                           name=name + "_Conv2DTranspose_" + str(unit))(y)
            else:
                y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                                  name=name + "_Conv2D_" + str(unit))(y)
            if batchnorm:
                y = layers.BatchNormalization()(y)
    else:
        # Block of a Conv2D layer followed by an UpSampling2D layer followed by num-1 Conv2D layers
        if block > 0:
            y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                              name=name + '_Conv2D_0')(y)
            if batchnorm:
                y = layers.BatchNormalization()(y)
        y = layers.UpSampling2D((2, 2), name=name + '_UpSampling2D')(y)
        for unit in range(1, block):
            y = layers.Conv2D(filters, kernel_size, activation=activation, padding='same',
                              name=name + '_Conv2D_' + str(unit))(y)
            if batchnorm:
                y = layers.BatchNormalization()(y)
    return y


def _encoder_model(input_shape=(),
                   stack=(),
                   stack_filters=(),
                   latent_filters=1,
                   kernel_size=(3, 3),
                   conv_transpose=False,
                   up_first=False,
                   residual=False,
                   batchnorm=False,
                   dense_units=(),
                   activation='relu',
                   encoder_activation='linear',
                   ):
    if len(stack) == 0 and len(dense_units) == 0:
        print("You should have minimum 1 convolutional or 1 dense layer")
        exit(1)
    if len(stack) > 1 and len(input_shape) != 3:
        print("Length input_shape should be 3 with convolutional layers")
        exit(1)
    if len(stack) == 0 and len(input_shape) != 1:
        print("Length input_shape should be 1 if only dense layers")
        exit(1)
    if len(stack) != len(stack_filters):
        print("stack and stack_filters should have the same length")
        exit(1)
    if len(stack) > 1 and input_shape[0] % (2 ** len(stack)) != 0:
        print("input_shape[0] should be a multiple of 2^len(stack)")
        exit(1)
    if len(stack) > 1 and input_shape[1] % (2 ** len(stack)) != 0:
        print("input_shape[1] should be a multiple of 2^len(stack)")
        exit(1)
    if not up_first and residual:
        print("Residual only possible with UpSampling layer first in decoder")
        exit(1)
    if residual and conv_transpose:
        print("Residual not possible with Conv2DTranspose layer in decoder")
        exit(1)
    if not up_first and conv_transpose:
        print("Transposed convolution only possible with UpSampling layer first in decoder")
        exit(1)

    x = Input(input_shape, name="Encoder_Input")
    y = x

    # Encoder blocks with Conv2D or residual units and a MaxPooling layer
    block_nr = 1
    for block, filters in zip(stack, stack_filters):
        y = _encoder_block(y, block=block, filters=filters, kernel_size=kernel_size, residual=residual,
                           batchnorm=batchnorm, activation=activation, name='Enc_' + str(block_nr))
        block_nr += 1

    # Encoder dense layers
    if len(dense_units) != 0:
        if len(stack) > 0:
            y = layers.Flatten()(y)
        for layer, units in enumerate(dense_units):
            if layer != len(dense_units) - 1:
                y = layers.Dense(units, activation=activation,
                                 name='Enc_' + str(block_nr) + '_Dense_' + str(layer))(y)
            else:  # last layer has other activation
                y = layers.Dense(units, activation=encoder_activation,
                                 name='Enc_' + str(block_nr) + '_Dense_' + str(layer))(y)
    # If no dense layers, last Conv2D layer
    else:
        y = layers.Conv2D(latent_filters, kernel_size, activation=encoder_activation, padding='same',
                          name='Enc_' + str(block_nr) + '_Conv2D_0')(y)

    model = Model(x, y, name="Encoder")
    return model


def _decoder_model(input_shape=(),
                   stack=(),
                   stack_filters=(),
                   latent_filters=1,
                   kernel_size=(3, 3),
                   conv_transpose=False,
                   up_first=False,
                   residual=False,
                   batchnorm=False,
                   dense_units=(),
                   activation='relu',
                   decoder_activation='linear',
                   ):
    # Nbr of blocks in en/decoder
    block_nr = len(stack) + 1
    # Input shape of decoder
    comp_factor = 2 ** len(stack_filters)
    if len(dense_units) == 0 and len(stack) != 0:  # only convolutional layers
        decoder_input_shape = (input_shape[0] // comp_factor, input_shape[1] // comp_factor, latent_filters)
    elif len(stack) != 0:  # convolutional and dense layers
        decoder_input_shape = (dense_units[-1])
        conv_output_shape = (input_shape[0] // comp_factor, input_shape[1] // comp_factor, stack_filters[-1])
    else:  # only dense layers
        decoder_input_shape = dense_units[-1]

    x = Input(shape=decoder_input_shape, name="Decoder_Input")
    y = x

    # Decoder dense layers
    if len(dense_units) != 0:
        if len(dense_units) > 1:
            for layer, units in enumerate(dense_units[-2::-1]):
                y = layers.Dense(units, activation=activation,
                                 name='Dec_' + str(block_nr) + '_Dense_' + str(len(dense_units) - layer - 1))(y)
        if len(stack) != 0:
            # Last dense layer units should match conv layer
            y = layers.Dense(_prod(conv_output_shape), name='Dec_' + str(block_nr) + '_Dense_0')(y)
            # Shape of encoder output after convolution
            y = layers.Reshape(conv_output_shape)(y)
        else:
            y = layers.Dense(input_shape[0], name='Dec_' + str(block_nr) + '_Dense_0')(y)
        block_nr -= 1

    # Decoder blocks with Conv2D layers or residual elements and an UpSampling layer
    for block, filters in zip(stack[::-1], stack_filters[::-1]):
        if len(dense_units) != 0 and block_nr == len(stack):
            # Fist block has 1 conv layer less in case of a dense block
            y = _decoder_block(y, block=block - 1, filters=filters, conv_transpose=conv_transpose,
                               kernel_size=kernel_size,
                               residual=residual, batchnorm=batchnorm, activation=activation, up_first=up_first,
                               name='Dec_' + str(block_nr))
        else:
            y = _decoder_block(y, block=block, filters=filters, conv_transpose=conv_transpose, kernel_size=kernel_size,
                               residual=residual, batchnorm=batchnorm, activation=activation, up_first=up_first,
                               name='Dec_' + str(block_nr))
        block_nr -= 1

    # Last Conv2D layer
    if len(stack) != 0:
        y = layers.Conv2D(input_shape[-1], kernel_size, activation=decoder_activation, padding='same',
                          name='Dec_' + str(block_nr) + '_Conv2D_0')(y)

    model = Model(x, y, name="Decoder")
    return model


if __name__ == "__main__":
    # Test scenarios for creating models
    hyper_params = [{"input_shape": [8, 8, 1], "stack": [1, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": False},
                    {"input_shape": [8, 8, 1], "stack": [1, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True},
                    {"input_shape": [8, 8, 1], "stack": [1, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True, "conv_transpose": True},
                    {"input_shape": [8, 8, 1], "stack": [1, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True, "residual": True},
                    {"input_shape": [8, 8, 1], "stack": [3, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": False},
                    {"input_shape": [8, 8, 1], "stack": [3, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True},
                    {"input_shape": [8, 8, 1], "stack": [3, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True, "conv_transpose": True},
                    {"input_shape": [8, 8, 1], "stack": [3, ], "stack_filters": [32, ],
                     "dense_units": (), "up_first": True, "residual": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": (), "up_first": False},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": (), "up_first": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": (), "up_first": True, "conv_transpose": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": (), "up_first": True, "residual": True},
                    {"input_shape": [8, ], "dense_units": [20, 10]},
                    {"input_shape": [8, 8, 1], "stack": [2, ], "stack_filters": [32, ],
                     "dense_units": [20, 10], "up_first": False},
                    {"input_shape": [8, 8, 1], "stack": [2, ], "stack_filters": [32, ],
                     "dense_units": [20, 10], "up_first": True},
                    {"input_shape": [8, 8, 1], "stack": [2, ], "stack_filters": [32, ],
                     "dense_units": [20, 10], "up_first": True, "conv_transpose": True},
                    {"input_shape": [8, 8, 1], "stack": [2, ], "stack_filters": [32, ],
                     "dense_units": [20, 10], "up_first": True, "residual": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": [20, 10], "up_first": False},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": [20, 10], "up_first": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": [20, 10], "up_first": True, "conv_transpose": True},
                    {"input_shape": [8, 8, 1], "stack": [1, 1], "stack_filters": [32, 16],
                     "dense_units": [20, 10], "up_first": True, "residual": True},
                    ]
    build_model = build_ae  # build_ae or build_diresa
    for hyper_param in hyper_params:
        print("\n\n", hyper_param)
        model = build_model(**hyper_param)
        model.summary(expand_nested=True)
