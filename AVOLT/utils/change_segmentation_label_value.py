# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
from AVOLT.utils.niftireader import load_image
import nibabel as nib
import numpy as np


def change_segmentation_value_to255(filepath_img):

    img = nib.load(filepath_img)
    img_np = img.get_fdata()
    img_np[img_np == 1] = 255
    new_labeled_img = nib.Nifti1Image(img_np.astype(np.uint8), affine=img.affine, header=img.header)
    nib.save(new_labeled_img, filepath_img)


