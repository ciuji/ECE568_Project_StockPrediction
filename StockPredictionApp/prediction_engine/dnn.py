"""Regression using the DNN Regressor Estimator."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import random

STEPS = 1000
PRICE_NORM_FACTOR = 10
DAY_SECONDS = 86400


class DNN(object):

    @staticmethod
    def pre_process(X: np.ndarray, y: np.ndarray, x: np.ndarray):
        x = X[0] - x
        X = X[0] - X
        X = X / DAY_SECONDS
        x = x / DAY_SECONDS

        # print(y[50])
        # x = np.asarray(X[50]).reshape(-1, 1)
        # print(x)
        # X = X[:50]
        # y = y[:50]

        # get the training set and cross-valid set
        rate = 1 # typically 0.7
        l1 = random.sample(list(range(X.shape[0])), int(len(X) * rate))
        x_train = X[l1]
        y_train = y[l1]
        l2 = list(set(list(range(X.shape[0]))) - set(l1))
        x_test = X[l2]
        y_test = y[l2]

        x_train_dist = {"time": x_train}
        x_test_dist = {"time": x_test}
        x_dist = {"time": x}

        train = tf.data.Dataset.from_tensor_slices((dict(x_train_dist), y_train))
        test = tf.data.Dataset.from_tensor_slices((dict(x_test_dist), y_test))
        to_predict_x = tf.data.Dataset.from_tensor_slices(dict(x_dist))

        # Switch the labels to units of thousands for better convergence.
        def normalize_price(features, labels):
            return features, labels / PRICE_NORM_FACTOR

        train = train.map(normalize_price)
        test = test.map(normalize_price)

        return train, test, to_predict_x

    @staticmethod
    def predict(X: np.ndarray, y: np.ndarray, x: np.ndarray):
        (train, test, to_predict_x) = DNN.pre_process(X, y, x)
        # Build the training input_fn.
        def input_train():
            return (
                # Shuffling with a buffer larger than the data set ensures
                # that the examples are well mixed.
                train.shuffle(1000).batch(128)
                # Repeat forever
                .repeat().make_one_shot_iterator().get_next())

        # Build the validation input_fn.
        def input_test():
            return (test.shuffle(1000).batch(128)
                    .make_one_shot_iterator().get_next())

        feature_columns = [
            tf.feature_column.numeric_column(key="time")
        ]

        # Build a DNNRegressor, with 2x20-unit hidden layers, with the feature columns
        # defined above as input.
        model = tf.estimator.DNNRegressor(
            hidden_units=[20, 20],
            feature_columns=feature_columns,
            optimizer=tf.train.ProximalAdagradOptimizer(
                learning_rate=0.3, #512, 256, 0.008, norm_factor = 1
                l1_regularization_strength=0.001
            )
        )

        def predict_fn():
            return to_predict_x.make_one_shot_iterator().get_next()

        # Train the model.
        model.train(input_fn=input_train, steps=STEPS)
        prediction = model.predict(input_fn=predict_fn)
        prediction = list(prediction)
        print(prediction[0]['predictions'][0] * PRICE_NORM_FACTOR)
        # for p in enumerate(prediction):
        #     print(p[1]['predictions'][0])

        # Evaluate how the model performs on data it has not yet seen.
        eval_result = model.evaluate(input_fn=input_test)

        # The evaluation returns a Python dictionary. The "average_loss" key holds the
        # Mean Squared Error (MSE).
        average_loss = eval_result["average_loss"]

        # Convert MSE to Root Mean Square Error (RMSE).
        print("\n" + 80 * "*")
        print("\nRMS error for the test set: ${:.0f}"
              .format(PRICE_NORM_FACTOR * average_loss**0.5))

        print()
        return prediction[0]['predictions'][0] * PRICE_NORM_FACTOR
