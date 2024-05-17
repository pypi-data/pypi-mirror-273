# Tests the sampler module

import pytest

from astrosampler import Sampler


def test_sampler_abstract():
    """
    Checks that the base Sampler class cannot be instantiated.
    """
    with pytest.raises(TypeError):
        Sampler()
