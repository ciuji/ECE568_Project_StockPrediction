import numpy as np


class VolatilityRatio(object):

    @staticmethod
    def indicator(price: np.float_, historical_price: np.ndarray, historical_volume: np.ndarray) -> np.float_:
        A = np.sum(historical_volume[np.where(price > historical_price)])
        D = np.sum(historical_volume[np.where(price < historical_price)])
        U = np.sum(historical_volume[np.where(price == historical_price)])

        return np.float_((A + U / 2) / (A + D + U))
