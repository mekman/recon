from __future__ import absolute_import, division, print_function
import os.path as op
# import numpy as np
# import pandas as pd
import numpy.testing as npt
import recon as re

data_path = op.join(re.__path__[0], 'data')


def test_cum_gauss():
    G = re.gaussian_receptive_field(x0=1., y0=3., s0=1., amplitude=1.)

    # A basic test that the input and output have the same shape:
    npt.assert_equal(G.shape, (32, 32))
