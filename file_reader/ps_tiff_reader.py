import os

from osgeo import gdal
import numpy as np
from model.pol_sar_data import PolSARData
from constants.polarization_constant import (FULL_POLARIZATION, DUAL_POLARIZATION, FULL_POLARIZATION_CHANNELS,
                                             DUAL_POLARIZATION_CHANNELS)


gdal.UseExceptions()

C_path = '.\dat_tiff\C'
S_path = '.\data_tiff\S'
datasets = []


def pre_process(dir_path, file_dict):
    """
    Get the shape of data matrix
    :return: Shape
    """
    if file_dict is not None:
        dataset = gdal.Open(f'{dir_path}/{file_dict.get(next(iter(file_dict)))}', gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        dataset = None
        return data.shape


def read_tiff_full_as_SAR(dir_path, file_dict, row, col):
    """
    Read .tiff files with full_polarization channels
    :param col:
    :param row:
    :param dir_path:
    :param file_dict:
    :return: S_matrix
    """
    shape = (row, col)
    for polar in FULL_POLARIZATION_CHANNELS:
        file_name = file_dict[polar]
        file_path = os.path.join(dir_path, file_name)
        dataset = gdal.Open(file_path, gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        if data.shape != shape:
            raise Exception('channel size error')
        dataset = None
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    return SAR_matrix


def read_tiff_dual_as_SAR(dir_path, file_dict, col, row, dual_type: str):
    """
    Read .tiff files with dual_polarization channels
    :param row:
    :param col:
    :param file_dict:
    :param dir_path:
    :param dual_type: the type of dual_polarization constant e.g. 'PP1'
    :return: S_matrix
    """
    shape = pre_process(dir_path, file_dict)
    for polar in DUAL_POLARIZATION_CHANNELS[dual_type]:
        file_name = file_dict[polar]
        file_path = os.path.join(dir_path, file_name)
        dataset = gdal.Open(file_path, gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        if data.shape != shape:
            raise Exception('channel size error')
        dataset = None
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    return SAR_matrix


if __name__ == '__main__':
    read_tiff_dual_as_SAR('PP1')
