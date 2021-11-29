# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import pydicom

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import nibabel as nib


#def remove_noise(filepath_img):
filepath_img = r"C:\develop\AVOLT\data\T01_L02_perfect_overlap_0mm_margin_Ablation.nii.gz"
img = nib.load(filepath_img)
img_np = img.get_fdata()
imageSegm_nda_NonZero = img_np.nonzero()
num_voxels = len(list(zip(imageSegm_nda_NonZero[0],
                          imageSegm_nda_NonZero[1],
                          imageSegm_nda_NonZero[2])))
# morphology.dilation creates a segmentation of the image
# If one pixel is between the origin and the edge of a square of size
# 5x5, the pixel belongs to the same class

# We can instead use a circule using: morphology.disk(2)
# In this case the pixel belongs to the same class if it's between the origin
# and the radius
img_np[img_np == 255] = 1
mask = ndimage.morphology.binary_fill_holes(img_np)
#img_np = ndimage.morphology.binary_dilation(mask, np.ones((3, 3)))
img_np[img_np == 1] = 255

new_labeled_img = nib.Nifti1Image(img_np.astype(np.uint8), affine=img.affine, header=img.header)
nib.save(new_labeled_img, filepath_img)
