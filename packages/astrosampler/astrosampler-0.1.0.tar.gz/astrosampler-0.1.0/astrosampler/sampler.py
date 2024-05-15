import abc
import numpy as np
from typing import Tuple, Optional


class Sampler(abc.ABC):
    """
    Sampler is a base class for all samplers. It provides a common interface for sampling data from a distribution.
    """
    def __init__(self, rng: np.random.Generator = np.random.default_rng()):
        self.rng = rng

    @abc.abstractmethod
    def sample(self, size: Optional[int | Tuple] = None) -> float | np.ndarray:
        """
        Samples data from this distribution.
        :param size: Accepts an integer or a tuple of integers. Specifies the shape of the output for multidimensional
         samplers, or the number of samples for one-dimensional samplers. If not specified, returns the float value for
          a single sample.
        :return: An array of samples from the distribution.
        """
        pass
