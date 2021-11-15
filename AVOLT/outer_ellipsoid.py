# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu (RMS)
"""
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
from skimage.draw import ellipsoid


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


def outer_ellipsoid_fit(img_file, tol=0.001):
    """
    Find the minimum volume ellipsoid enclosing (outside) a set of points.
    Return A, c where the equation for the ellipse given in "center form" is
    (x-c).T * A * (x-c) = 1
    """
    points = get_surface_points(img_file)
    points = np.asmatrix(points)
    N, d = points.shape
    Q = np.column_stack((points, np.ones(N))).T
    u = np.ones(N) / N
    err = 1 + tol
    while err > tol:
        X = Q * np.diag(u) * Q.T
        M = np.diag(Q.T * la.inv(X) * Q)
        jdx = np.argmax(M)
        step_size = (M[jdx] - d - 1.0) / ((d + 1) * (M[jdx] - 1.0))
        new_u = (1 - step_size) * u
        new_u[jdx] += step_size
        err = la.norm(new_u - u)
        u = new_u

    c = u * points  # center of ellipsoid
    A = la.inv(points.T * np.diag(u) * points - c.T * c) / d
    #return np.asarray(A), np.squeeze(np.asarray(c))
    U, D, V = la.svd(np.asarray(A))
    rx, ry, rz = 1. / np.sqrt(D)
    return rx, ry, rz


def volume_ellipsoid_spacing(a, b, c, spacing):
    """

    :param a: major semi-axis of an ellipsoid
    :param b: least semi-axis of an ellipsoid
    :param c:  minor semi-axis of an ellipsoid
    :param spacing: spacing of a grid, tuple like e.g. (1,  1, 1)
    :return: volume of an ellipsoid in ml, taking spacing into account
    """
    ellipsoid_array = ellipsoid(a, b, c, spacing)
    ellipsoid_non_zero = ellipsoid_array.nonzero()
    num_voxels = len(list(zip(ellipsoid_non_zero[0],
                              ellipsoid_non_zero[1],
                              ellipsoid_non_zero[2])))
    volume_object_ml = (num_voxels * spacing[0] * spacing[1] * spacing[2]) / 1000

    return volume_object_ml


def get_outer_volume_ml(img_file):
    rx, ry, rz = outer_ellipsoid_fit(img_file)
    dcm_img = sitk.ReadImage(img_file)
    spacing = dcm_img.GetSpacing()
    vol_outer_ellipsoid = volume_ellipsoid_spacing(rx, ry, rz, spacing)
    return vol_outer_ellipsoid


def plot_ellipsoid(A, centroid, color, ax):
    """

    :param A: matrix
    :param centroid: center
    :param color: color
    :param ax: axis
    :return:
    """
    centroid = np.asarray(centroid)
    A = np.asarray(A)
    U, D, V = la.svd(A)
    rx, ry, rz = 1. / np.sqrt(D)
    u, v = np.mgrid[0:2 * np.pi:20j, -np.pi / 2:np.pi / 2:10j]
    x = rx * np.cos(u) * np.cos(v)
    y = ry * np.sin(u) * np.cos(v)
    z = rz * np.sin(v)
    E = np.dstack((x, y, z))
    E = np.dot(E, V) + centroid
    x, y, z = np.rollaxis(E, axis=-1)
    ax.plot_wireframe(x, y, z, cstride=1, rstride=1, color=color, alpha=0.2)
    ax.set_zlabel('Z-Axis')
    ax.set_ylabel('Y-Axis')
    ax.set_xlabel('X-Axis')


