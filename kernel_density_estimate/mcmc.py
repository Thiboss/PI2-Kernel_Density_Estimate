from imports import *
from kernel_density_estimate.kde import kernel_density_estimate

def MCMC_bandwidth(data, initial_bandwidth, normal_std, iterations):
    mu,sigma = data.mean(), data.std()
    current_bandwidth = initial_bandwidth
    accepted_samples = []
    acceptance_rates = []
    total_proposals = 0
    accepted_proposals = 0
    h_list = []

    for _ in range(iterations):
        # Generate a new proposal for bandwidth
        proposed_bandwidth = np.random.normal(current_bandwidth, normal_std)

        # Calculate the likelihoods for current and proposed bandwidths
        current_likelihood = np.prod(kernel_density_estimate(data, data, current_bandwidth))
        proposed_likelihood = np.prod(kernel_density_estimate(data, data, proposed_bandwidth))

        # Calculate the prior probabilities for current and proposed bandwidths
        current_prior = norm.pdf(current_bandwidth)  # Example prior assuming a normal distribution
        proposed_prior = norm.pdf(proposed_bandwidth)  # Example prior assuming a normal distribution

        # Calculate the acceptance probability
        acceptance_prob = min(1, (proposed_likelihood * proposed_prior) / (current_likelihood * current_prior))

        # Accept or reject the proposal based on the acceptance probability
        if np.random.uniform() < acceptance_prob:
            current_bandwidth = proposed_bandwidth
            accepted_samples.append(current_bandwidth)
            accepted_proposals += 1
            h_list.append(proposed_bandwidth)
        else:
          h_list.append(current_bandwidth)

        total_proposals += 1
        acceptance_rate = accepted_proposals / total_proposals
        acceptance_rates.append(acceptance_rate)

    return accepted_samples, acceptance_rates, h_list