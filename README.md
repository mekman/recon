[![Build Status](https://travis-ci.org/mekman/recon.svg?branch=master)](https://travis-ci.org/mekman/recon)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/mekman/recon?branch=master&svg=true)](https://ci.appveyor.com/project/mekman/recon/history)
[![DOI](https://zenodo.org/badge/84972499.svg)](https://zenodo.org/badge/latestdoi/84972499)

## recon

Recon is an open-source python module for (pRF-based) stimulus reconstruction
analyses from fMRI data.

### Quick-start

    import matplotlib.pyplot as plt
    import recon as re

    # load prf properties
    x0, y0, s0, beta = re.load_example_prf_data()

    # reconstruct stimulus
    S = re.stimulus_reconstruction(x0, y0, s0, beta, method='summation')

    plt.imshow(S)


### Installation

You can install the ``recon`` package with:

    pip install -U recon


### Citing

If you use the project please cite this article:

    Ekman, Kok & de Lange (2017). Time-compressed preplay of anticipated events
    in human primary visual cortex. Nature Communications.
