import numpy as np
from astrosampler import SalpeterIMF


def test_salpeter_imf():
    """
    Checks that the Salpeter IMF sampler samples correctly.
    """
    rng = np.random.default_rng(seed=1)
    imf = SalpeterIMF(mass_range=(0.08, 100), rng=rng)

    # Generate 100 samples of 10000 stars for testing
    for i in range(100):
        samples = imf.sample(size=10000)

        # Check minimum and maximum values
        assert np.min(samples) >= 0.08
        assert np.max(samples) <= 100

        # Check that mean is near expected value (0.28315)
        assert np.isclose(np.mean(samples), 0.283, atol=0.05)
