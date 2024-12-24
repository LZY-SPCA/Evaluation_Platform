import os.path

from model.pol_sar_data import PolSARData
from constants.polarization_constant import FULL_POLARIZATION, DUAL_POLARIZATION
from constants.polarization_constant import GENERATE_OUTPUT
from util.constant_process import get_generate_details
import numpy as np

from util.file_discover import config_reader

"""
    该文件直接读取PolSARpro所允许读入的数据类型
    目前有S2,C3,T3
"""


def join_file_name(generate_type):
    output_path = get_generate_details(generate_type)
    file = {}
    mask_file = []
    for mask in output_path.mask.item():
        mask_file.append(mask)
    file['mask'] = mask_file
    visible_file = []
    for visible in output_path.visible.item():
        visible_file.append(visible)
    file['visible'] = visible_file
    return file


def C3_matrix_input(input_path, pol_sar_data):
    """
    Generate C3-matrix from polarization data.
    :return:
    """
    channel_num = 3

    row, col, polar_type = config_reader(input_path)
    shape = (row, col)
    matrix_set = []
    for i in range(1, channel_num + 1):
        for j in range(1, channel_num + 1):
            if i == j:
                file_path = os.path.join(input_path, f'C{i}{j}.bin')
                matrix = np.fromfile(file_path, dtype=np.float32)
                matrix = matrix.reshape((shape[0], shape[1]))
                matrix_set.append(matrix)
            if i < j:
                real_path = os.path.join(input_path, f'C{i}{j}_real.bin')
                imag_path = os.path.join(input_path, f'C{i}{j}_imag.bin')
                real_data = np.fromfile(real_path, dtype=np.float32)
                imag_data = np.fromfile(imag_path, dtype=np.float32)
                real_data = real_data.reshape((shape[0], shape[1]))
                imag_data = imag_data.reshape((shape[0], shape[1]))
                matrix = real_data + 1j * imag_data
                matrix_set.append(matrix)
            if i > j:
                matrix_set.append(np.zeros(shape))
    C_matrix = np.dstack(matrix_set)
    C_matrix = C_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 3, 3)
    pol_sar_data.set_C_matrix(C_matrix)


def T3_matrix_input(input_path, pol_sar_data):
    """
    Input T3-matrix from polarization data.
    :return:
    """
    channel_num = 3
    row, col, polar_type = config_reader(input_path)
    shape = (row, col)
    matrix_set = []
    for i in range(1, channel_num + 1):
        for j in range(1, channel_num + 1):
            if i == j:
                file_path = os.path.join(input_path, f'T{i}{j}.bin')
                matrix = np.fromfile(file_path, dtype=np.float32)
                matrix = matrix.reshape((shape[0], shape[1]))
                matrix_set.append(matrix)
            if i < j:
                real_path = os.path.join(input_path, f'T{i}{j}_real.bin')
                imag_path = os.path.join(input_path, f'T{i}{j}_imag.bin')
                real_data = np.fromfile(real_path, dtype=np.float32)
                imag_data = np.fromfile(imag_path, dtype=np.float32)
                real_data = real_data.reshape((shape[0], shape[1]))
                imag_data = imag_data.reshape((shape[0], shape[1]))
                matrix = real_data + 1j * imag_data
                matrix_set.append(matrix)
            if i > j:
                matrix_set.append(np.zeros(shape))
    T_matrix = np.dstack(matrix_set)
    T_matrix = T_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 3, 3)
    pol_sar_data.set_T_matrix(T_matrix)


def S2_matrix_input(input_path, pol_sar_data):
    """
    Input S2-matrix from polarization data.
    :return:
    """
    channel_num = 2
    row, col, polar_type = config_reader(input_path)
    shape = (row, col)
    matrix_set = []
    for i in range(1, channel_num + 1):
        for j in range(1, channel_num + 1):
            file_path = os.path.join(input_path, f'S{i}{j}.bin')
            matrix = np.fromfile(file_path, dtype=np.float32)
            matrix = matrix.reshape((row, col, 2))
            real_part = matrix[:, :, 0]
            imag_part = matrix[:, :, 1]
            # 合成复数数据
            dataset = real_part + 1j * imag_part
            matrix_set.append(dataset)
    S_matrix = np.dstack(matrix_set)
    S_matrix = S_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    pol_sar_data.set_S_matrix(S_matrix)


if __name__ == '__main__':
    pol_sar_data = PolSARData('111', 5000, 5894, 'full')
    T3_matrix_input('/全极化T3/T3', pol_sar_data)
    print(pol_sar_data.is_T_matrix_available())

    S2_matrix_input(r'/full S2/S2', pol_sar_data)
    print(pol_sar_data.is_S_matrix_available())
