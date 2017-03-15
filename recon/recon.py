import numpy as np
from .due import due, Doi

__all__ = ["gaussian_receptive_field"]


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
