import numpy as np
from .due import due, Doi

__all__ = ["select_prf", "gaussian_receptive_field", "stimulus_reconstruction",
           "example_prf_data"]


# Use duecredit (duecredit.org) to provide a citation to relevant work to
# be cited. This does nothing, unless the user has duecredit installed,
# And calls this with duecredit (as in `python -m duecredit script.py`):
due.cite(Doi("10.1167/13.9.30"),
         description="Template project for small scientific Python projects",
         tags=["reference-implementation"],
         path='shablona')


def gaussian_receptive_field(x0=0., y0=0., s0=1., amplitude=1.,
                             extent=[-8, 8, -8, 8], resolution=0.5,
                             norm=False):
    """Gaussian 2D receptive field

    Parameters
    ----------
    x0 : float
         Center of gaussian in visual degrees (default=0).
    y0 : float
         Center of gaussian in visual degrees (default=0).
    s0 : float
         Size of gaussian in visual degrees (default=1)
    amplitude : float
         Amplitude (default=1.)
    extent : scalars (left, right, bottom, top), default: [-8, 8, -8, 8]
         Screen dimensions in visual degrees.
    resolution : float
         Interpolation steps in visual degrees (default=0.5).
    norm : bool
        Normalize gaussian to unit area under the curve (default=False).

    Examples
    --------
    >>> G = gaussian_receptive_field(x0=1., y0=3., s0=1., amplitude=1.)
    >>> G.shape
    (32, 32)
    """

    xmin, xmax, ymin, ymax = extent
    xv = np.arange(xmin, xmax, resolution)
    yv = np.arange(ymin, ymax, resolution)
    [X, Y] = np.meshgrid(xv, yv)
    Y = np.flipud(Y)

    s_factor2 = 2. * s0**2
    gauss = amplitude * np.exp(-((X-x0)**2 + (Y-y0)**2)/s_factor2)

    if norm:
        gauss /= gauss.sum()

    return gauss


def example_prf_data(n_voxel=100, dataset='noise', seed=42):
    """returns toy example data-set

    Parameters
    ----------
    n_voxel : integer
        Number of voxel included in the example dataset (default=100).
    dataset : string ['noise']
        Dataset to load (default='noise').

    Returns
    -------
    x0 : array
         Center of gaussian in visual degrees.
    y0 : array
         Center of gaussian in visual degrees.
    s0 : array
         Size of gaussian in visual degrees.
    betas : array
         Voxel activations.

    Examples
    --------
    >>> x0, y0, s0, r2, betas = example_prf_data()
    >>> plt.scatter(x0, y0, c='r', edgecolor='')
    """
    # TODO implement more toy datasets
    from scipy.spatial.distance import euclidean

    rng = np.random.RandomState(seed)

    if dataset is not 'noise':
        raise NotImplementedError('Selected dataset is not implemented')
    else:
        x0 = rng.normal(size=n_voxel)
        y0 = rng.normal(size=n_voxel)
        r2 = np.ones(n_voxel)
        betas = rng.normal(size=n_voxel, scale=0.2)

        # rf become larger with distance from Fovea
        s0 = np.zeros(n_voxel)
        for i in range(n_voxel):
            s0[i] = euclidean([0, 0], [x0[i], y0[i]])

    return x0, y0, s0, r2, betas


def select_prf(data, r2_thr=5., s0_thr=2.5, extent=[-8, 8, -8, 8],
               verbose=True):
    """select voxel based on prf-properties

    Parameters
    ----------
    data : class
        pRF data (x0, y0, s0, R2).

    Examples
    --------
    >>> x0, y0, s0, r2, betas = example_prf_data()
    >>> x0, y0, s0, idx = select_prf()
    """

    n_voxel = data.x0.size
    xmin, xmax, ymin, ymax = extent

    selection = np.zeros(n_voxel)
    selection[data.r2 >= r2_thr] += 1
    selection[data.s0 <= s0_thr] += 1
    selection[data.y0 >= ymin] += 1
    selection[data.y0 <= ymax] += 1
    selection[data.x0 >= xmin] += 1
    selection[data.x0 <= xmax] += 1

    idx = np.where(selection == 6)[0]

    if verbose:
        print 'Selected voxel:', len(idx)

    x0 = data.x0[idx]
    y0 = data.y0[idx]
    s0 = data.s0[idx]
    return x0, y0, s0, idx


def stimulus_reconstruction(x0, y0, s0, betas, method='summation',
                            extent=[-8, 8, -8, 8]):
    """prf-based stimulus reconstruction

    Parameters
    ----------
    x0 : array
         Centers of gaussian in visual degrees.
    y0 : array
         Centers of gaussian in visual degrees.
    s0 : array
         Sizes of gaussian in visual degrees.
    betas : array
        Voxel activations.
    method : string ['summation'|'multi']
        Reconstruction method to use (default='summation').
    extent : scalars (left, right, bottom, top), default: [-8, 8, -8, 8]
         Screen dimensions in visual degrees.

    Examples
    --------
    >>> #TODO
    """

    if not method == 'summation':
        raise NotImplementedError('Only method=summation is supported ATM')

    n_voxel = x0.shape[0]

    # TODO make sure x0 shape == y0 == s0
    assert len(x0) == len(y0)

    if method == 'summation':
        xmin, xmax, ymin, ymax = extent
        resolution = 0.2
        xv = np.arange(xmin, xmax, resolution)
        yv = np.arange(ymin, ymax, resolution)
        [X, Y] = np.meshgrid(xv, yv)
        Y = np.flipud(Y)

        xdim = xv.shape[0]
        ydim = yv.shape[0]

        S = np.zeros((n_voxel, xdim, ydim))
        for i in range(n_voxel):
            S[i] = gaussian_receptive_field(x0[i], y0[i], s0[i], betas[i],
                                            extent, resolution)

        return S.mean(0).reshape(xdim, ydim)
