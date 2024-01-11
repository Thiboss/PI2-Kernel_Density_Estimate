from imports import *
from kernel_density_estimate.kde import dynamic_kernel_cdf

def Z(returns, t, h, w, t0):
  return dynamic_kernel_cdf(returns, returns[t], h, w, t0)

def k_uniformity(Z_vals, t0):
    T = len(Z_vals)
    maximum = 0
    for s in range(t0+1,T):
      somme = 0
      for u in range(t0+1,T):
          if (Z_vals[u] >= 0) and (Z_vals[u] <= Z_vals[s]):
            somme += 1
      diff = Z_vals[s] - (1/(T-t0+1)) * somme
      if abs(diff) > maximum:
        maximum = abs(diff)
    return maximum

def k_independence(Z_vals, t0, tau):
    T = len(Z_vals)
    maximum = 0
    for s in range(t0+1, T-tau):
      somme = 0
      for u in range(t0+1,T-tau):
        if (Z_vals[u] >= 0) and (Z_vals[u] <= Z_vals[s]) and (Z_vals[u+tau] >= 0) and (Z_vals[u+tau] <= Z_vals[s+tau]):
          somme += 1
      diff = Z_vals[s]*Z_vals[s+tau] - (1/(T-tau-t0+1)) * somme
      if abs(diff) > maximum:
        maximum = abs(diff)
    return maximum

def k_global(Z_vals, t0, tau):
  if tau == 0:
    k = k_uniformity(Z_vals, t0)
  else:
    k = k_independence(Z_vals, t0, tau)
  return k

def d_nu(Z_vals, t0, nu):
    T = len(Z_vals)
    max_val = float('-inf')
    for tau in range(nu+1):
        statistic =(((T - tau - t0)**0.5)* k_global(Z_vals, t0, tau))
        if statistic > max_val:
            max_val = statistic
    return max_val

def pit_bandwidth(returns, t0 = 500, nu = 22):

    min_statistic = float('inf')
    h_PIT = None
    w_PIT = None

    h_values = np.linspace(0.3, 0.8, 6)
    w_values = np.linspace(1-(1/nu), 0.99, 15)

    for h in h_values:
        for w in w_values:
            Z_vals = [Z(returns, t, h, w, t0) for t in range(t0+1, len(returns))]
            statistic = d_nu(Z_vals, t0, nu)
            if statistic < min_statistic:
                min_statistic = statistic
                h_PIT = h
                w_PIT = round(w,3)

    print("Best h:", h_PIT)
    print("Best w:", w_PIT)
    return h_PIT, w_PIT