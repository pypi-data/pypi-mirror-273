import numpy as np
from modelbest_sdk.dataset.sampler.sampler import Sampler


class WeightedSampler(Sampler):
    def __init__(self, weights, seed):
        self.weights = weights
        self.n_samples = len(weights)
        np.random.seed(seed)
        
    def __call__(self):
        return np.random.choice(self.n_samples, p=self.weights)