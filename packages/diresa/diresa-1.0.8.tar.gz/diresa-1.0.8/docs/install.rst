.. _install:

Install *DIRESA*
================

**Overview**

*DIRESA* is a Python package for dimension reduction based on TensorFlow_.
The distance-regularized Siamese twin autoencoder architecture is designed
to preserve distance (ordering) in latent space while capturing the non-linearities in
the datasets.

.. _TensorFlow: https://www.tensorflow.org

**Prerequisites**

The *DIRESA* package depends on the tensorflow_ and tensorflow_probability_ packages. 
These can be installed with the following commands:

.. code-block:: bash

  pip install tensorflow
  pip install tensorflow_probability

.. _tensorFlow: https://www.tensorflow.org
.. _tensorflow_probability: https://www.tensorflow.org/probability

**Install DIRESA**

Install *DIRESA* with the following command:

.. code-block:: bash

  pip install diresa