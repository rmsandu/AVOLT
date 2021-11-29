# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import SimpleITK as sitk
import nibabel as nib


class ResizeSegmentation(object):

    def __init__(self, segmentation_mask_filepath, img_source_filepath):
        self.segmentation_mask = sitk.ReadImage(segmentation_mask_filepath)
        self.img_source = sitk.ReadImage(img_source_filepath)

    def resample_segmentation(self):
        """
        If the spacing of the segmentation is different from its original image, use RESAMPLE
        Resample parameters:  identity transformation, zero as the default pixel value, and nearest neighbor interpolation
        (assuming here that the origin of the original segmentation places it in the correct location w.r.t  original image)
        :return: new_segmentation of the image_roi
        """
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(self.img_source)
        resampler.SetDefaultPixelValue(0)
        # use NearestNeighbor interpolation for the ablation&tumor segmentations so no new labels are generated
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        resampler.SetSize(self.img_source.GetSize())
        resampler.SetOutputSpacing(self.img_source.GetSpacing())
        resampler.SetOutputDirection(self.img_source.GetDirection())
        resampled_mask = resampler.Execute(self.segmentation_mask)  # the tumour mask
        return resampled_mask

