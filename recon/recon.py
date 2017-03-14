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


def gaussian_receptive_field(X=None, Y=None, x0=0., y0=0., s0=1., amplitude=1.,
                             norm=False):
    """Gaussian 2D receptive field

    Parameters
    ----------
    X :
    Y :
    x0 : float
         Center on x-axis (default=0).
    y0 : float
         Center on y-axis (default=0).
    s0 : float
         Size in SD (default=1)
    amplitude : float
         Amplitude (default=1.)
    norm : bool
        Normalize gaussian (default=False).

    Examples
    --------
    >>> G = gaussian_receptive_field(X=None, Y=None, x0=0., y0=0., s0=1.,
        amplitude=1.)
    >>> G.shape
    (32, 32)
    """

    if X is None:
        # results in 40,40
        xv = np.arange(-8, 8, 0.5)  # decrease 0.5 for finer resolution
        yv = np.arange(-8, 8, 0.5)
        [X, Y] = np.meshgrid(xv, yv)
        Y = np.flipud(Y)

    s_factor2 = 2.*s0**2
    gauss = amplitude * np.exp(-((X-x0)**2 + (Y-y0)**2)/s_factor2)

    if norm:
        gauss /= gauss.sum()

    return gauss
