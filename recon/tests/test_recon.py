from __future__ import absolute_import, division, print_function
import os.path as op
import numpy as np
import numpy.testing as npt
import recon as re

data_path = op.join(re.__path__[0], 'data')


def test_gaussian_receptive_field():
    G = re.gaussian_receptive_field(x0=1., y0=3., s0=1., amplitude=1.)

    # A basic test that the input and output have the same shape:
    npt.assert_equal(G.shape, (32, 32))


def test_example_prf_data():
    x0, y0, s0, r2, betas = re.example_prf_data(n_voxel=10)
    npt.assert_equal(x0.shape[0], 10)


# def test_select_prf():
#     select_prf()

def test_stimulus_reconstruction():
    x0 = np.random.normal(size=100)
    y0 = np.random.normal(size=100)
    s0 = np.random.normal(size=100)

    betas = np.ones(100)

    S = re.stimulus_reconstruction(x0, y0, s0, betas, method='summation',
                                   extent=[-8, 8, -8, 8])

    # TODO: make propper test
    npt.assert_equal(S.shape, (32, 32))
