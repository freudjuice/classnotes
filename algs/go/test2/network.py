from tensorflow.contrib.keras import regularizers as R
from tensorflow.contrib.keras import models as M
from tensorflow.contrib.keras import layers as L
from tensorflow.contrib.keras import backend as K
from util import flatten_idx, random_transform, idx_transformations
import numpy as np, util, random

class PolicyValue:
    """uses a convolutional neural network to evaluate the state of the game
    and compute a probability distribution over the next action
    and value of the current state.
    """

    def __init__(self, model):
        self.model = model

    def batch_eval_value_state(self, states):
        return np.array([random.random() for x in states])        

    def eval_policy_state(self, state, moves=None):
        return [(action, random.random()) for action in state.get_legal_moves()]

    def eval_value_state(self, state):
        x = util.get_board(state)
        x1 = x.reshape(1, 17, 9, 9)
        print x1.shape
        return self.model.predict(x1)

    @staticmethod
    def create_network(**kwargs):
        """construct a convolutional neural network with Residual blocks.
        Arguments are the same as with the default CNNPolicy network, except the default
        number of layers is 20 plus a new n_skip parameter

        Keword Arguments:
        - input_dim:             depth of features to be processed by first layer (default 17)
        - board:                 width of the go board to be processed (default 19)
        - filters_per_layer:     number of filters used on every layer (default 256)
        - layers:                number of residual blocks (default 19)
        - filter_width:          width of filter
                                 Must be odd.
        """
        defaults = {
            "input_dim": 17,
            "board": 9,
            "filters_per_layer": 16,
            "layers": 4,
            "filter_width": 3
        }
        # copy defaults, but override with anything in kwargs
        params = defaults
        params.update(kwargs)

        # create the network using Keras' functional API,
        model_input = L.Input(shape=(params["input_dim"], params["board"], params["board"]))

        # create first layer
        convolution_path = L.Convolution2D(
            input_shape=(),
            filters=params["filters_per_layer"],
            kernel_size=params["filter_width"],
            activation='linear',
            padding='same',
            kernel_regularizer=R.l2(.0001),
            bias_regularizer=R.l2(.0001))(model_input)

        convolution_path = L.BatchNormalization(
                beta_regularizer=R.l2(.0001),
                gamma_regularizer=R.l2(.0001))(convolution_path)

        convolution_path = L.Activation('relu')(convolution_path)

        def add_resnet_unit(path, **params):
            """Add a resnet unit to path
            Returns new path
            """

            block_input = path
            # add Conv2D
            path = L.Convolution2D(
                filters=params["filters_per_layer"],
                kernel_size=params["filter_width"],
                activation='linear',
                padding='same',
                kernel_regularizer=R.l2(.0001),
                bias_regularizer=R.l2(.0001))(path)
            # add BatchNorm
            path = L.BatchNormalization(
                    beta_regularizer=R.l2(.0001),
                    gamma_regularizer=R.l2(.0001))(path)
            # add ReLU
            path = L.Activation('relu')(path)
            # add Conv2D
            path = L.Convolution2D(
                filters=params["filters_per_layer"],
                kernel_size=params["filter_width"],
                activation='linear',
                padding='same',
                kernel_regularizer=R.l2(.0001),
                bias_regularizer=R.l2(.0001))(path)
            # add BatchNorm
            path = L.BatchNormalization(
                    beta_regularizer=R.l2(.0001),
                    gamma_regularizer=R.l2(.0001))(path)
            # Merge 'input layer' with the path
            path = L.Add()([block_input, path])
            # add ReLU
            path = L.Activation('relu')(path)
            return path

        # create all other layers
        for _ in range(params['layers']):
            convolution_path = add_resnet_unit(convolution_path, **params)

        # policy head
        policy_path = L.Convolution2D(
            input_shape=(),
            filters=2,
            kernel_size=1,
            activation='linear',
            padding='same',
            kernel_regularizer=R.l2(.0001),
            bias_regularizer=R.l2(.0001))(convolution_path)
        policy_path = L.BatchNormalization(
                beta_regularizer=R.l2(.0001),
                gamma_regularizer=R.l2(.0001))(policy_path)
        policy_path = L.Activation('relu')(policy_path)
        policy_path = L.Flatten()(policy_path)
        policy_path = L.Dense(
                params["board"]*params["board"]+1,
                kernel_regularizer=R.l2(.0001),
                bias_regularizer=R.l2(.0001))(policy_path)
        policy_output = L.Activation('softmax')(policy_path)

        # value head
        value_path = L.Convolution2D(
            input_shape=(),
            filters=1,
            kernel_size=1,
            activation='linear',
            padding='same',
            kernel_regularizer=R.l2(.0001),
            bias_regularizer=R.l2(.0001))(convolution_path)
        value_path = L.BatchNormalization(
                beta_regularizer=R.l2(.0001),
                gamma_regularizer=R.l2(.0001))(value_path)
        value_path = L.Activation('relu')(value_path)
        value_path = L.Flatten()(value_path)
        value_path = L.Dense(
                256,
                kernel_regularizer=R.l2(.0001),
                bias_regularizer=R.l2(.0001))(value_path)
        value_path = L.Activation('relu')(value_path)
        value_path = L.Dense(
                1,
                kernel_regularizer=R.l2(.0001),
                bias_regularizer=R.l2(.0001))(value_path)
        value_output = L.Activation('tanh')(value_path)

        return M.Model(inputs=[model_input], outputs=[policy_output, value_output])
