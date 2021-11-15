# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu (RMS)
"""
import SimpleITK as sitk
from mpl_toolkits.mplot3d import axes3d
import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np
#import sklearn.datasets
from scipy.spatial import ConvexHull
import numpy.linalg as la
from math import pi


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


def GetHull(points):
    dim = points.shape[1]
    hull = ConvexHull(points)
    A = hull.equations[:, 0:dim]
    b = hull.equations[:, dim]
    return A, -b, hull  # Negative moves b to the RHS of the inequality


def FindMaximumVolumeInscribedEllipsoid(img_file):
    """Find the inscribed ellipsoid of maximum volume. Return its matrix-offset form."""
    points = get_surface_points(img_file)
    dim = points.shape[1]
    A, b, hull = GetHull(points)

    B = cp.Variable((dim, dim), PSD=True)  # Ellipsoid
    d = cp.Variable(dim)  # Center

    constraints = [cp.norm(B @ A[i], 2) + A[i] @ d <= b[i] for i in range(len(A))]
    prob = cp.Problem(cp.Minimize(-cp.log_det(B)), constraints)
    optval = prob.solve()
    if optval == np.inf:
        raise Exception("No solution possible!")
        return None
    print(f"Optimal value: {optval}")
    ball_vol = 4 / 3.0 * np.pi * (1.0 ** 3)
    # ax = Plot(points, hull, B.value, d.value)
    # return B.value, d.value, ax
    vol_formula_inner = np.sqrt(la.det(B.value) / 1000) * ball_vol
    return vol_formula_inner

