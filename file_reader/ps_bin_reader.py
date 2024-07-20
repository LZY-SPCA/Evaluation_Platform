"""
    Read .bin files and convert them into PolSARData.
"""
import os

from model.pol_sar_data import PolSARData
import numpy as np
from constants.polarization_constant import (BIN_FULL_POLARIZATION_CHANNELS, FULL_POLARIZATION, DUAL_POLARIZATION,
                                             BIN_DUAL_POLARIZATION_CHANNELS)

bin_file_path = './bin/full/'
datasets = []


def read_bin_full_as_SAR(dir_path, real_dict, imag_dict, row: int, col: int):
    """
    Read .bin files with full_polarization channels
    :param dir_path:
    :param real_dict:
    :param imag_dict:
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :return: S_matrix
    """
    shape = (row, col)
    for polar in BIN_FULL_POLARIZATION_CHANNELS:
        real_path = os.path.join(dir_path, real_dict[polar])
        imag_path = os.path.join(dir_path, imag_dict[polar])
        real_data = np.fromfile(real_path, dtype=np.float32)
        imag_data = np.fromfile(imag_path, dtype=np.float32)
        print(real_data.shape)
        if not (real_data.size == row * col and imag_data.size == row * col):
            raise Exception('channels not same size')
        real_part = real_data.reshape((row, col))
        imag_part = imag_data.reshape((row, col))
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    return SAR_matrix


def read_bin_dual_as_SAR(dir_path, real_dict, imag_dict,row: int, col: int, dual_type: str):
    """
    Read .bin files with dual_polarization channels
    :param dir_path:
    :param real_dict:
    :param imag_dict:
    :param row: the row of the data matrix
    :param col: the column of the data matrix
    :param dual_type: the type of dual_polarization constant e.g. 'PP1'
    :return: S_matrix
    """
    shape = (row, col)
    for polar in BIN_DUAL_POLARIZATION_CHANNELS[dual_type]:
        real_path = os.path.join(dir_path, real_dict[polar])
        imag_path = os.path.join(dir_path, imag_dict[polar])
        real_data = np.fromfile(real_path, dtype=np.float32)
        imag_data = np.fromfile(imag_path, dtype=np.float32)
        print(real_data.shape)
        if not (real_data.size == row * col and imag_data.size == row * col):
            raise Exception('channels not same size')
        real_part = real_data.reshape((row, col))
        imag_part = imag_data.reshape((row, col))
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    SAR_matrix = np.dstack((datasets[0], datasets[1]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    return SAR_matrix


def read_T_bin_as_SAR(row: int, col: int, dir_path, polar_type):
    if polar_type is FULL_POLARIZATION:
        channel_num = 3
    else:
        channel_num = 2
    shape = (row, col)
    matrix_set = []
    for i in range(1, channel_num + 1):
        for j in range(1, channel_num + 1):
            if i == j:
                file_path = os.path.join(dir_path, f'T{i}{j}.bin')
                matrix = np.fromfile(file_path, dtype=np.float32)
                matrix = matrix.reshape((shape[0], shape[1]))
                matrix_set.append(matrix)
            if i < j:
                real_path = os.path.join(dir_path, f'T{i}{j}_real.bin')
                imag_path = os.path.join(dir_path, f'T{i}{j}_imag.bin')
                real_data = np.fromfile(real_path, dtype=np.float32)
                imag_data = np.fromfile(imag_path, dtype=np.float32)
                real_data = real_data.reshape((shape[0], shape[1]))
                imag_data = imag_data.reshape((shape[0], shape[1]))
                matrix = real_data + 1j * imag_data
                matrix_set.append(matrix)
            if i > j:
                matrix_set.append(np.zeros(shape))
    T_matrix = np.dstack(matrix_set)
    if polar_type is FULL_POLARIZATION:
        T_matrix = T_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 3, 3)
    else:
        T_matrix = T_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    return T_matrix


if __name__ == '__main__':
    read_bin_dual_as_SAR(5000, 5894, 'PP1')
