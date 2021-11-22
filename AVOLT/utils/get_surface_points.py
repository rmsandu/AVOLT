# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import SimpleITK as sitk
import numpy as np


def get_surface_points(img_file):
    """
    :param img_file: image filepath
    :return: surface points of a 3d volume
    """
    dcm_img = sitk.ReadImage(img_file)
    x_spacing, y_spacing, z_spacing = dcm_img.GetSpacing()
    contour = sitk.LabelContour(dcm_img, fullyConnected=False)
    contours = sitk.GetArrayFromImage(contour)
    vertices_locations = contours.nonzero()
    vertices_unravel = list(zip(vertices_locations[0], vertices_locations[1], vertices_locations[2]))
    vertices_list = [list(vertices_unravel[i]) for i in range(0, len(vertices_unravel))]

    surface_points = np.array(vertices_list)
    surface_points = surface_points.astype(np.float64)
    # surface_points[:, 0] *= x_spacing/10
    # surface_points[:, 1] *= y_spacing/10
    # surface_points[:, 2] *= z_spacing/10
    return surface_points
