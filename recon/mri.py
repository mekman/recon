#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib

__all__ = ['load_mri', 'save_mri']


def load_mri(func, mask):
    """load MRI voxel data

    The data is converted into a 2D (n_voxel, n_tps) array.

    Parameters
    ----------
    func : string
        Path to imaging data (e.g. nifti).
    mask : string
        Path to binary mask (e.g. nifti) that defines brain regions. Values > 0
        are regarded as brain tissue.

    Returns
    -------
    ts : ndarray, shape(n_voxel, n_tps)
        Timeseries information in a 2D array.

    See Also
    --------
    save_mri: save MRI voxel data to disk.

    Examples
    --------
    >>> ts = load_mri(func='localizer.nii.gz', mask='V1_mask.nii.gz')
    """

    # load mask data
    m = nib.load(mask).get_data()

    # load func data
    d = nib.load(func).get_data()

    # mask the data
    func_data = d[m != 0] # nib.load(func).get_data()[nib.load(mask).get_data()!=0]

    del d

    return func_data


def save_mri(data, mask, fname=None):
    """save MRI voxel data

    Parameters
    ----------
    data : ndarray, shape(n_voxel,) **or** shape(n_voxel, n_tps)
       Voxel data to save to disk.
    mask : string
        Path to binary mask (e.g. nifti) that defines brain regions. Values > 0
        are regarded as brain tissue.
    fname : string
        Filename.

    Examples
    --------
    >>> ts = load_mri(func='localizer.nii.gz', mask='V1_mask.nii.gz')
    >>> ts = ts + 1. # some operation
    >>> save_mri(ts, 'V1_mask.nii.gz', 'localizer_plus_one.nii.gz')
    """
    # load mask data
    f = nib.load(mask)
    m = f.get_data()
    aff = f.get_affine()

    s = m.shape
    if len(data.shape) == 2:
        n_tps = data.shape[1]
    else:
        n_tps = 1
        data = data[:, np.newaxis]

    res = np.zeros((s[0], s[1], s[2], n_tps)) # + time
    res[m != 0] = data

    # save to disk
    if not fname is None:
        nib.save(nib.Nifti1Image(res, aff), fname)
