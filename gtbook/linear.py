# AUTOGENERATED! DO NOT EDIT! File to edit: ../linear.ipynb.

# %% auto 0
__all__ = ['vv', 'denoising_MRF']

# %% ../linear.ipynb 3
import numpy as np
import gtsam
from gtsam import noiseModel
from .display import show

from typing import Dict

# %% ../linear.ipynb 6
def vv(keys_vectors: Dict[int, np.ndarray]):
    """Create a VectorValues from a dict"""
    result = gtsam.VectorValues()
    for j, v in keys_vectors.items():
        result.insert(j, v)
    return result

# %% ../linear.ipynb 10
def denoising_MRF(M: int, N: int, sigma = 0.5, smoothness_sigma=0.5):
    """Create MxN MRF
        @returns graph and symbols used for rows.
        
    """
    row_symbols = [chr(ord('a')+row) for row in range(M)]
    keys = {(row, col): gtsam.symbol(row_symbols[row], col+1)
            for row in range(M) for col in range(N)}
    
    rng = np.random.default_rng(42)
    data = rng.normal(loc=0, scale=sigma, size=(M, N, 1))
    data_model = noiseModel.Isotropic.Sigmas([sigma])

    smoothness_model = noiseModel.Isotropic.Sigmas([smoothness_sigma])

    I = np.eye(1, 1, dtype=float)
    zero = np.zeros((1, 1))
    graph = gtsam.GaussianFactorGraph()
    for row in range(M):
        for col in range(N):
            # add data terms:
            j = keys[(row, col)]
            graph.add(j, I, np.array(data[row, col]), data_model)
            # add smoothness terms:
            if col > 0:
                j1 = keys[(row, col-1)]
                graph.add(j, I, j1, -I, zero, smoothness_model)
            if row > 0:
                j2 = keys[(row-1, col)]
                graph.add(j, I, j2, -I, zero, smoothness_model)

    return graph, row_symbols

# %% ../linear.ipynb 13
#| export
