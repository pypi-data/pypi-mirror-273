# Astro Sampler

Sample from distributions commonly used in astronomy.

## Installation

```bash
pip install astrosampler
```

### Dependencies

- `numpy`

## Usage

```python
from astrosampler import SalpeterIMF

# Sample 1000 stellar masses from the Salpeter (1955) IMF
imf = SalpeterIMF(mass_range=(0.08, 100))
masses = imf.sample(1000)
```
