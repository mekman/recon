from __future__ import absolute_import, division, print_function
import os.path as op
import numpy as np
# import pandas as pd
import numpy.testing as npt
import recon as sb

data_path = op.join(sb.__path__[0], 'data')


def test_cum_gauss():
    G = sb.gaussian_receptive_field(X=None, Y=None, x0=0., y0=0., s0=1.,
                                    amplitude=1.)

    # A basic test that the input and output have the same shape:
    npt.assert_equal(G.shape, (32,32))
