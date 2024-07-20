"""
    Read .dat files and convert them into PolSARData.
"""
import os
from osgeo import gdal
import numpy as np
from constants.polarization_constant import (FULL_POLARIZATION, DUAL_POLARIZATION, FULL_POLARIZATION_CHANNELS,
                                             DUAL_POLARIZATION_CHANNELS)
from model.pol_sar_data import PolSARData

gdal.UseExceptions()

C_path = './dat/C'
S_path = './dat/S'
dat_file_path = f'{C_path}/1144_010_C_HH_L1A.dat'
datasets = []


def read_dat_full_as_SAR(dir_path, file_dict, row: int, col: int):
    """
    Read .dat files with full_polarization channels
    :param file_dict:
    :param dir_path:
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :return: S_matrix
    """
    shape = (row, col)
    for polar in FULL_POLARIZATION_CHANNELS:
        file_name = file_dict[polar]
        file_path = os.path.join(dir_path, file_name)
        dataset = np.fromfile(file_path, dtype=np.float32)
        if not dataset.size == 2 * row * col:
            raise Exception('channels not same size')
        dataset = dataset.reshape((row, col, 2))
        real_part = dataset[:, :, 0]
        imag_part = dataset[:, :, 1]
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    return SAR_matrix


def read_dat_dual_as_SAR(dir_path, file_dict, row: int, col: int, dual_type: str):
    """
    Read .dat files with dual_polarization channels
    :param file_dict:
    :param dir_path:
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :param dual_type: the type of dual_polarization constant e.g. 'PP1'
    :return: S_matrix
    """
    shape = (row, col)
    for polar in DUAL_POLARIZATION_CHANNELS[dual_type]:
        file_name = file_dict[polar]
        file_path = os.path.join(dir_path, file_name)
        dataset = np.fromfile(file_path, dtype=np.float32)
        if not dataset.size == 2 * row * col:
            raise Exception('channels error size')
        dataset = dataset.reshape((row, col, 2))
        real_part = dataset[:, :, 0]
        imag_part = dataset[:, :, 1]
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    SAR_matrix = np.dstack((datasets[0], datasets[1]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    return SAR_matrix


if __name__ == '__main__':
    read_dat_full_as_SAR(5000, 5894)
    read_dat_dual_as_SAR(5000, 5894, dual_type='PP1')
