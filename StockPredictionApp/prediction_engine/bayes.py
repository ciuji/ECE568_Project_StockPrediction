import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures


class Bayes(object):

    @staticmethod
    def calculate_score(deg, X, y):
        pipe = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(deg),
            BayesianRidge(normalize=False)
        )  # type: Pipeline

        pipe.fit(X, y)
        return pipe.score(X, y)

    @staticmethod
    def predict(X: np.ndarray, y: np.ndarray, x: np.ndarray):

        s = None
        d = 3

        for i in range(50):
            sc = Bayes.calculate_score(i, X, y)
            # print(i, sc)
            if s is None or sc > s:
                s = sc
                d = i

        pipe = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(d),
            BayesianRidge(normalize=False)
        )  # type: Pipeline

        pipe.fit(X, y)

        return pipe.predict(x)
