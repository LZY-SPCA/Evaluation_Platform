from osgeo import gdal
import numpy as np
from model.pol_sar_data import PolSARData
from constants.polarization_constant import (FULL_POLARIZATION, DUAL_POLARIZATION, FULL_POLARIZATION_CHANNELS,
                                             DUAL_POLARIZATION_CHANNELS)


gdal.UseExceptions()

C_path = '.\dat_tiff\C'
S_path = '.\data_tiff\S'
full_polarisation_mode = ['HH', 'HV', 'VH', 'VV']
dual_polarisation_mode = ['HH', 'VV']
datasets = []


def pre_process():
    """
    Get the shape of data matrix
    :return: Shape
    """
    dataset = gdal.Open(f'{C_path}/1144_010_C_HH_L1A.tiff', gdal.GA_ReadOnly)
    data = dataset.GetRasterBand(1).ReadAsArray()
    return data.shape


def read_tiff_full_as_SAR(file_path, file_name) -> PolSARData:
    """
    Read .tiff files with full_polarization channels
    :param file_path:
    :param file_name:
    :return: PolSARData
    """
    shape = pre_process()
    for polar in FULL_POLARIZATION_CHANNELS:
        dataset = gdal.Open(f'{C_path}/1144_010_C_{polar}_L1A.tiff', gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1], FULL_POLARIZATION)
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


def read_tiff_dual_as_SAR(dual_type: str) -> PolSARData:
    """
    Read .tiff files with dual_polarization channels
    :param dual_type: the type of dual_polarization constant e.g. 'PP1'
    :return: PolSARData
    """
    shape = pre_process()
    for polar in DUAL_POLARIZATION_CHANNELS[dual_type]:
        dataset = gdal.Open(f'{C_path}/1144_010_C_{polar}_L1A.tiff', gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1],
                          DUAL_POLARIZATION, dual_type)
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


if __name__ == '__main__':
    read_tiff_dual_as_SAR('PP1')
