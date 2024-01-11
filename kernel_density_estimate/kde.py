from imports import *
from amise import scott_bandwidth, silverman_bandwidth
from loocv import LOOCV_bandwidth
from mcmc import MCMC_bandwidth
from conditional import conditional_bandwidth
from complexity import complexity_bandwidth
from pit import pit_bandwidth

def triweight(x):
    return (35/32) * (1 - x**2)**3 * (np.abs(x) <= 1)

def epa(x):
    return 0.75 * (1 - x**2) if np.abs(x) <= 1 else 0

def bi(x):
  return (15/16) * ((1 - x)**2)**2 * (np.abs(x) <= 1)

def kernel_density_estimate(data, x, bandwidth, kernel='gaussian'):

    for i in range(len(data)):
      if kernel == 'gaussian':
          kernel_vals = norm.pdf(((x - data[i]) / bandwidth))
      elif kernel == 'tri':
          kernel_vals = triweight((x - data[i]) / bandwidth)
      elif kernel == 'epa':
          u = (x - data[i]) / bandwidth
          kernel_vals = 0.75 * (1 - u**2) * (np.abs(u) <= 1)
      elif kernel == "bi":
          kernel_vals = bi((x - data[i]) / bandwidth)
      else:
          raise ValueError("Invalid kernel type. Available options: 'gaussian', 'tri', 'epa'")

    return kernel_vals / (len(data) * bandwidth)

def dynamic_kernel_cdf(data, x, bandwidth, w, t0):
    t = len(data)
    kernel_vals_cdf =  0
    for i in range(t0):
      kernel_vals_cdf += w**(t0-i) * norm.cdf(((x - data[i]) / bandwidth)) * ((1 - w) / (1 - w**t0))
    for i in range(t0+1,t):
      kernel_vals_cdf = w * kernel_vals_cdf + (1 - w) * norm.cdf(((x - data[i]) / bandwidth))
    return kernel_vals_cdf

def recursive_dynamic_kernel(data, x, bandwidth, w, t0):
    t = len(data)
    weight = ((1 - w) * w ** (t - t0)) / (1 - w ** t0)
    kernel_vals = weight * norm.pdf(((x - data[t0]) / bandwidth)) / bandwidth
    for i in range(t0+1,t):
      kernel_vals = w * kernel_vals + ((1 - w) / bandwidth) * norm.pdf(((x - data[i]) / bandwidth))
    return kernel_vals

def compute_kde(x_values, returns, method = "scott"):
    
    match method:

        case "scott":
            bandwidth = scott_bandwidth(returns)
        case 'silverman':
            bandwidth = silverman_bandwidth(returns)
        case "loocv":
            penalty= 1/len(returns)**0.5
            bandwidth = LOOCV_bandwidth(returns, np.linspace(0.1, 1, 20) , penalty)
        case "mcmc":
            accepted_samples, acceptance_rates,h_list = MCMC_bandwidth(returns, silverman_bandwidth(returns), 0.2 , 1000)
            bandwidth = round(np.mean(accepted_samples), 3)
        case "complexity":
            bandwidth = complexity_bandwidth(returns)
        case "pit":
            bandwidth, omega = pit_bandwidth(returns, 500, 22)
        case "conditional":
            bandwidth = conditional_bandwidth(returns)
            
    if method == 'pit':
        KDE = [recursive_dynamic_kernel(returns, x, bandwidth, omega, 500) for x in x_values]
    else:
        KDE = [kernel_density_estimate(returns, x, bandwidth) for x in x_values]

    return KDE