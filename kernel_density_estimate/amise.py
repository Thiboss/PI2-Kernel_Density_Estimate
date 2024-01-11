from imports import *

def scott_bandwidth(data):
    n = len(data)
    sigma = data.std()
    bandwidth = 1.06 * sigma * n**(-0.2)
    return bandwidth

def silverman_bandwidth(data):
    n = len(data)
    sigma = data.std()
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    bandwidth = 0.9 * np.minimum(sigma, iqr/1.34) * n**(-0.2)
    return bandwidth