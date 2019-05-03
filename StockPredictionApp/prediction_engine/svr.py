from os import cpu_count

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


class SupportVectorRegression(object):

    @staticmethod
    def predict(X: np.ndarray, y: np.ndarray, x: np.ndarray):
        pipe = make_pipeline(
            StandardScaler(),
            SVR()
        )

        grid_search = GridSearchCV(
            pipe,
            param_grid={
                'svr__gamma': np.logspace(-2, 2, 5),
                'svr__C': [1e0, 1e1, 1e2, 1e3]
            },
            n_jobs=cpu_count(),
            cv=X.shape[0] // 10,
            verbose=0
        )

        grid_search.fit(X, y)

        return grid_search.predict(x)
