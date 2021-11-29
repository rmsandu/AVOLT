# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu (RMS)
"""
import SimpleITK as sitk
from mpl_toolkits.mplot3d import axes3d
import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import numpy.linalg as la
import AVOLT.utils.get_surface_points as pts


def GetHull(points):
    dim = points.shape[1]
    hull = ConvexHull(points)
    A = hull.equations[:, 0:dim]
    b = hull.equations[:, dim]
    return A, -b, hull  # Negative moves b to the RHS of the inequality


def FindMaximumVolumeInscribedEllipsoid(img_file):
    """Find the inscribed ellipsoid of maximum volume. Return its matrix-offset form."""
    points = pts.get_surface_points(img_file)
    dim = points.shape[1]
    A, b, hull = GetHull(points)

    B = cp.Variable((dim, dim), PSD=True)  # Ellipsoid
    d = cp.Variable(dim)  # Center

    constraints = [cp.norm(B @ A[i], 2) + A[i] @ d <= b[i] for i in range(len(A))]
    prob = cp.Problem(cp.Minimize(-cp.log_det(B)), constraints)
    optval = prob.solve()
    if optval == np.inf:
        return -1
        # raise Exception("No solution possible!")
    print(f"Optimal value: {optval}")
    ball_vol = 4 / 3.0 * np.pi * (1.0 ** 3)
    # ax = Plot(points, hull, B.value, d.value)
    # return B.value, d.value, ax
    # vol_formula_inner = np.sqrt(la.det(B.value) / 1000) * ball_vol
    vol_formula_inner = (np.linalg.det(B.value) * ball_vol) / 1000
    return vol_formula_inner

