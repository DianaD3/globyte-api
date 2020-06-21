from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import IsolationForest
import numpy as np

def forecast(input, steps):
    # Returns a 1D array of steps length with forecasted values from input array
    #
    # step = 2
    # input = [1, 2, 3, 4, 5]
    # output = [6, 7]
    model = ARIMA(input, order=(4,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast(steps)
    return output[0]

def anomaly_detection(input):
    # Returns a 1D array of same length as input with 1 for normal and -1 for anomalies
    #
    # input = [1, 2, 1, 2, 1, 100, 1, 2, 1]
    # output = [1, 1, 1, 1, 1, -1, 1, 1, 1]
    input = np.asarray(input).reshape(-1, 1)
    clf = IsolationForest()
    clf.fit(input)
    output = clf.predict(input)
    return output
