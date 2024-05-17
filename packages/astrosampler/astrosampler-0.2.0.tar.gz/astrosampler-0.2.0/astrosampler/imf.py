# Sample from various initial mass functions (IMFs)

from typing import Optional, Tuple

import numpy as np
from .sampler import Sampler


class SalpeterIMF(Sampler):
    """
    Samples from the Salpeter 1955 IMF (Bibcode: 1955ApJ...121..161S)
    which follows a power law with index -2.35.
    """
    def __init__(self, mass_range: Tuple[float, float] = (0.08, 150), rng: np.random.Generator = np.random.default_rng()):
        """
        Samples from the Salpeter 1955 IMF (Bibcode: 1955ApJ...121..161S)
        which follows a power law with index -2.35.
        :param mass_range: Defines the valid mass range for this sampler (default: (0.08, 150))
        :param rng: The random number generator to use (default: numpy.random.default_rng())
        """
        super().__init__(rng)
        self.mass_range = mass_range

    def sample(self, size: Optional[int | Tuple] = None) -> float | np.ndarray:
        prob = self.rng.uniform(size=size)
        return (prob * self.mass_range[1]**-1.35 + (1 - prob) * self.mass_range[0]**-1.35)**(1/-1.35)
