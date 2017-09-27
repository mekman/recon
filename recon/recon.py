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


def select_prf(x0, y0, s0, r2=None, r2_thr=5., s0_thr=2.5,
               extent=[-8, 8, -8, 8], verbose=True):
    """select voxel based on prf-properties

    Parameters
    ----------
    x0 : array, shape(n_voxel, )
         Center of gaussian in visual degrees.
    y0 : array, shape(n_voxel, )
         Center of gaussian in visual degrees.
    s0 : array, shape(n_voxel, )
         Size of gaussian in visual degrees.
    r2 : array, shape(n_voxel, ) | None
         Explained variance of pRF-model per voxel (default=None). Optional.
    r2_thr : int
         Positive R2 threshold (default=5.). Only voxel >= this value will be
         selected.
    s0_thr : int
         Positive s0 threshold (default=2.5). Only voxel <= this value will be
         selected.
    extent : list
        x0/y0 range; x0 (min,max), y0 (min/max). default=[-8, 8, -8, 8].
    verbose : bool
        Print information (default=True).

    Returns
    -------
    x0' : array, shape(n_voxel', )
         Center of gaussian in visual degrees.
    y0' : array, shape(n_voxel', )
         Center of gaussian in visual degrees.
    s0' : array, shape(n_voxel', )
         Size of gaussian in visual degrees.
    r2' : array, shape(n_voxel', )
         Explained variance of pRF-model per voxel.
    idx : list
         Indices of selected voxels.

    Examples
    --------
    >>> x0, y0, s0, r2, betas = example_prf_data()
    >>> x0, y0, s0, idx = select_prf(x0, y0, s0, r2)
    """

    n_voxel = x0.size
    xmin, xmax, ymin, ymax = extent

    # TODO assert that x0 shape == y0 shape etc
    if r2 is None:
        r2 = np.ones(n_voxel) + r2_thr

    selection = np.zeros(n_voxel)
    selection[r2 >= r2_thr] += 1
    selection[s0 <= s0_thr] += 1
    selection[y0 >= ymin] += 1
    selection[y0 <= ymax] += 1
    selection[x0 >= xmin] += 1
    selection[x0 <= xmax] += 1

    idx = np.where(selection == 6)[0]

    if verbose:
        print('Selected voxel: %s' % len(idx))

    x0 = x0[idx]
    y0 = y0[idx]
    s0 = s0[idx]
    r2 = r2[idx]

    return x0, y0, s0, r2, idx


def stimulus_reconstruction(x0, y0, s0, betas, method='summation',
                            extent=[-8, 8, -8, 8], resolution=0.5, clf=None):
    """prf-based stimulus reconstruction/inverse retinotopy

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
    method : string ['summation'|'multivariate']
        Reconstruction method to use (default='summation').
    extent : scalars (left, right, bottom, top), default: [-8, 8, -8, 8]
         Screen dimensions in visual degrees.
    resolution : float
         Interpolation steps in visual degrees (default=0.5).
    clf : class
        Classifier for ``multivariate`` method (default=None).

    Returns
    -------
    S : array, shape(n_pixel, n_pixel)
         Reconstructed image. ``n_pixel``depends on ``resolution`` parameter.

    Examples
    --------
    >>> x0, y0, s0, r2, betas = re.example_prf_data()
    >>> S = re.stimulus_reconstruction(x0, y0, s0, betas, method='summation')
    """

    n_voxel = x0.shape[0]

    # TODO make sure x0 shape == y0 == s0
    assert len(x0) == len(y0)

    xmin, xmax, ymin, ymax = extent
    xv = np.arange(xmin, xmax, resolution)
    yv = np.arange(ymin, ymax, resolution)
    [X, Y] = np.meshgrid(xv, yv)
    Y = np.flipud(Y)

    xdim = xv.shape[0]
    ydim = yv.shape[0]

    if method == 'summation':
        S = np.zeros((n_voxel, xdim, ydim))
        for i in range(n_voxel):
            S[i] = gaussian_receptive_field(x0[i], y0[i], s0[i], betas[i],
                                            extent, resolution)

        S = S.mean(0).reshape(xdim, ydim)

    elif method == 'multivariate':
        from sklearn import linear_model

        X = np.zeros((n_voxel, xdim * ydim))
        for i in range(n_voxel):
            X[i, :] = gaussian_receptive_field(x0[i], y0[i], s0[i]/1.,
                                               amplitude=1, extent=extent,
                                               resolution=resolution,
                                               norm=False).ravel()

        if clf is None:
            alphas = [0, 10, 20, 30, 50, 100]
            clf = linear_model.RidgeCV(alphas=alphas, cv=None,
                                       fit_intercept=True, gcv_mode=None,
                                       normalize=True, scoring=None,
                                       store_cv_values=False)

        clf.fit(X, betas)
        S = clf.coef_.reshape(xdim, xdim)

    else:
        raise NotImplementedError('Method not implemented')

    return S
