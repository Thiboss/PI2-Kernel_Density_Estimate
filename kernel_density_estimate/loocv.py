from imports import *
from kernel_density_estimate.kde import kernel_density_estimate

def MSE(true, pred):
  return np.mean((true - pred)**2)

def LOOCV_bandwidth(returns, bandwidths, penalty) :

  mse_scores = np.zeros_like(bandwidths)
  for i, h in enumerate(bandwidths):

    mse_total = 0

    for j in range(len(returns)):
      density = kernel_density_estimate(returns, returns[j], h)

      mse = MSE(returns[j], density)
      mse_total += mse

    mse_avg = mse_total/len(returns)
    mse_scores[i] = mse_avg + penalty*h

  return bandwidths[np.argmin(mse_scores)]