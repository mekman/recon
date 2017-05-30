[![Build Status](https://travis-ci.org/mekman/recon.svg?branch=master)](https://travis-ci.org/mekman/recon)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/mekman/recon?branch=master&svg=true)](https://ci.appveyor.com/project/mekman/recon/history)
[![Coverage Status](https://coveralls.io/repos/github/mekman/recon/badge.svg?branch=master)](https://coveralls.io/github/mekman/recon?branch=master)
[![DOI](https://zenodo.org/badge/84972499.svg)](https://zenodo.org/badge/latestdoi/84972499)

## recon

**Recon** is an open-source python module for (pRF-based) stimulus reconstruction
analyses from fMRI data. The main functions include:

- **simple reverse retinotopy** with the ``summation`` method (*Thirion et al. 2006; Kok & de Lange 2014; Ekman, Kok & de Lange 2017*)
- **advanced reverse retinotopy** with the ``multivariate`` method (*Ekman, Roelfsema & de Lange (in prep)*)
- **spatio-temporal reconstruction** (*Ekman, Kok & de Lange 2017*)
- tuning-curve **forward model** (*Brouwer & Heeger 2009*) - *in a future release*

### Quick-start

```shell
$ python
```
```python
>>> import matplotlib.pyplot as plt
>>> import recon as re
>>> # load prf properties
>>> x0, y0, s0, r2, betas = re.example_prf_data()
>>> # reconstruct stimulus
>>> S = re.stimulus_reconstruction(x0, y0, s0, betas, method='summation')
>>> plt.imshow(S)
```

### Installation

Currently this is only available through GitHub and source installation

    pip install git+https://github.com/mekman/recon.git --upgrade

or

    git clone git@github.com:mekman/recon.git
    cd recon
    python setup.py install

### Citing

If you use the project please cite this article:

    Ekman, Kok & de Lange (2017). Time-compressed preplay of anticipated events
    in human primary visual cortex. Nature Communications. 8, 15276 doi:
    10.1038/ncomms15276
