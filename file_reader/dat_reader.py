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


def read_dat_full_as_SAR(row: int, col: int) -> PolSARData:
    """
    Read .dat files with full_polarization channels
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :return: PolSARData
    """
    shape = (row, col)
    for polar in FULL_POLARIZATION_CHANNELS:
        dataset = np.fromfile(f'{C_path}/1144_010_C_{polar}_L1A.dat', dtype=np.float32)
        if not dataset.size == 2 * row * col:
            raise Exception('channels not same size')
        dataset = dataset.reshape((row, col, 2))
        real_part = dataset[:, :, 0]
        imag_part = dataset[:, :, 1]
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    print(datasets[0])
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    print(SAR_matrix)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1], FULL_POLARIZATION)
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


def read_dat_dual_as_SAR(row: int, col: int, dual_type: str) -> PolSARData:
    """
    Read .dat files with dual_polarization channels
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :param dual_type: the type of dual_polarization constant e.g. 'PP1'
    :return: PolSARData
    """
    shape = (row, col)
    for polar in DUAL_POLARIZATION_CHANNELS[dual_type]:
        dataset = np.fromfile(f'{C_path}/1144_010_C_{polar}_L1A.dat', dtype=np.float32)
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
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1],
                          DUAL_POLARIZATION, dual_type)
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


if __name__ == '__main__':
    read_dat_full_as_SAR(5000, 5894)
