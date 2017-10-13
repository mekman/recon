# from __future__ import absolute_import, division, print_function
# import os.path as op
import os
import numpy as np
import numpy.testing as npt
import nibabel as nib
import recon as re


def test_save_mri():
    # bad boy
    nii = nib.Nifti1Image(np.ones((5, 5, 5)), affine=np.identity(4))
    nib.save(nii, 'temp_mask.nii')
    re.save_mri(np.ones(5*5*5), 'temp_mask.nii', fname='temp_data.nii')
    data = re.load_mri('temp_data.nii', 'temp_mask.nii')
    os.remove('temp_mask.nii')
    os.remove('temp_data.nii')

    npt.assert_equal(np.ones((5*5*5, 1)), data)
