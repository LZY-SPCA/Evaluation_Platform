from pol_sar_data import PolSARData
import numpy as np
from constants.constant import (BIN_FULL_POLARIZATION_CHANNELS, FULL_POLARIZATION, DUAL_POLARIZATION,
                                BIN_DUAL_POLARIZATION_CHANNELS)

bin_file_path = './bin/full/'
datasets = []


def read_full_as_SAR(row: int, col: int) -> PolSARData:
    shape = (row, col)
    for polar in BIN_FULL_POLARIZATION_CHANNELS:
        real_data = np.fromfile(f'{bin_file_path}/{polar}_real.bin', dtype=np.float32)
        imag_data = np.fromfile(f'{bin_file_path}/{polar}_imag.bin', dtype=np.float32)
        print(real_data.shape)
        if not (real_data.size == row * col and imag_data.size == row * col):
            raise Exception('channels not same size')
        real_part = real_data.reshape((row, col))
        imag_part = imag_data.reshape((row, col))
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


def read_dual_as_SAR(row: int, col: int, dual_type: int) -> PolSARData:
    shape = (row, col)
    for polar in BIN_DUAL_POLARIZATION_CHANNELS[dual_type]:
        real_data = np.fromfile(f'{bin_file_path}/{polar}_real.bin', dtype=np.float32)
        imag_data = np.fromfile(f'{bin_file_path}/{polar}_imag.bin', dtype=np.float32)
        print(real_data.shape)
        if not (real_data.size == row * col and imag_data.size == row * col):
            raise Exception('channels not same size')
        real_part = real_data.reshape((row, col))
        imag_part = imag_data.reshape((row, col))
        # 合成复数数据
        dataset = real_part + 1j * imag_part
        datasets.append(dataset)
    print(datasets[0])
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    print(SAR_matrix)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1], DUAL_POLARIZATION, BIN_DUAL_POLARIZATION_CHANNELS[dual_type])
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data

if __name__ == '__main__':
    read_dual_as_SAR(5000, 5894, 0)
