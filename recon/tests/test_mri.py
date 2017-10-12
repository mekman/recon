# from __future__ import absolute_import, division, print_function
# import os.path as op
import numpy as np
import numpy.testing as npt
import nibabel as nib


def test_load_mri():
    # bad boy
    nii = nib.Nifti1Image(np.zeros((5, 5, 5)), affine=np.identity(4))
    npt.assert_equal(nii.affine, np.identity(4))


def test_save_mri():
    # bad boy
    npt.assert_equal((32, 32), (32, 32))
