# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
from enum import Enum

import numpy as np
import pandas as pd
from radiomics import featureextractor
from AVOLT.utils.change_segmentation_label_value import change_segmentation_value_to255
from AVOLT.utils.resample_segmentations import ResizeSegmentation
# from scipy import ndimage


class RadiomicsMetrics(object):

    def __init__(self, input_image, mask_image):
        self.input_image = input_image
        self.mask_image = mask_image
        self.error_flag = False

        class AxisMetricsRadiomics(Enum):
            center_of_mass_x, center_of_mass_y, center_of_mass_z, \
            center_of_mass_index_x, center_of_mass_index_y, center_of_mass_index_z, \
            elongation, sphericity, mesh_volume, volume_feature,  \
            diameter3D, diameter2D_slice, diameter2D_col, diameter2D_row, major_axis_length, \
            least_axis_length, minor_axis_length = range(17)

        axis_metrics_results = np.zeros((1, len(AxisMetricsRadiomics.__members__.items())))
        # %% Extract the diameter axis
        settings = {'label': 255, 'correctMask':True}
        extractor = featureextractor.RadiomicsFeatureExtractor(additionalInfo=True, **settings)
        try:
            result = extractor.execute(self.input_image, self.mask_image)
        except ValueError as e:
            if len(e.args) > 0 and e.args[0] == 'Label (255) not present in mask. Choose from [1]':
                change_segmentation_value_to255(mask_image)
                extractor = featureextractor.RadiomicsFeatureExtractor(additionalInfo=True, **settings)
                result = extractor.execute(self.input_image, self.mask_image)
            else:
                try:
                    resampling = ResizeSegmentation(mask_image, input_image)
                    self.mask_image = resampling.resample_segmentation()

                    result = extractor.execute(self.input_image, self.mask_image)
                except ValueError as e:
                    print("-----------------------------ERRORR-------------------")
                    print(repr(e))
                    print(self.input_image)
                    print(self.mask_image)
                    self.error_flag = True
                    return
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_x.value] = \
                result['diagnostics_Mask-original_CenterOfMass'][0]
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_y.value] = \
                result['diagnostics_Mask-original_CenterOfMass'][1]
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_z.value] = \
                result['diagnostics_Mask-original_CenterOfMass'][2]
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_x.value] = None
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_y.value] = None
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_z.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_x.value] = \
                result['diagnostics_Mask-original_CenterOfMassIndex'][0]
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_y.value] = \
                result['diagnostics_Mask-original_CenterOfMassIndex'][1]
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_z.value] = \
                result['diagnostics_Mask-original_CenterOfMassIndex'][2]
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_x.value] = None
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_y.value] = None
            axis_metrics_results[0, AxisMetricsRadiomics.center_of_mass_index_z.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.mesh_volume.value] = (result[
                                                                                   'original_shape_MeshVolume'].tolist()) / 1000
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.mesh_volume.value] = None
        # getMeshVolumeFeatureValue()
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.volume_feature.value] = (result[
                                                                              'original_shape_VoxelVolume'].tolist()) / 1000
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.volume_feature.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.elongation.value] = result['original_shape_Elongation']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.elongation.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.sphericity.value] = result['original_shape_Sphericity']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.sphericity.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter3D.value] = result['original_shape_Maximum3DDiameter']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter3D.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_slice.value] = result[
                'original_shape_Maximum2DDiameterSlice']  # euclidean
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_slice.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_col.value] = result[
                'original_shape_Maximum2DDiameterColumn']  # euclidean
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_col.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_row.value] = result[
                'original_shape_Maximum2DDiameterRow']  # euclidean
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.diameter2D_row.value] = None
        try:
            # PCA largest principal component
            axis_metrics_results[0, AxisMetricsRadiomics.major_axis_length.value] = result[
                'original_shape_MajorAxisLength']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.major_axis_length.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.least_axis_length.value] = result[
                'original_shape_LeastAxisLength']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.least_axis_length.value] = None
        try:
            axis_metrics_results[0, AxisMetricsRadiomics.minor_axis_length.value] = result[
                'original_shape_MinorAxisLength']
        except Exception:
            axis_metrics_results[0, AxisMetricsRadiomics.minor_axis_length.value] = None

        # %% Save to DataFrame
        self.axis_metrics_results_df = pd.DataFrame(data=axis_metrics_results, index=list(range(1)),
                                                    columns=[name for name, _ in
                                                             AxisMetricsRadiomics.__members__.items()])

    def get_axis_metrics_df(self):
        return self.axis_metrics_results_df
