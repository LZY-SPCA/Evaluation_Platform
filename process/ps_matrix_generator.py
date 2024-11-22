import os.path

from model.pol_sar_data import PolSARData
from constants.polarization_constant import FULL_POLARIZATION, DUAL_POLARIZATION
from constants.polarization_constant import GENERATE_OUTPUT
from util.constant_process import get_generate_details
import numpy as np

from util.file_discover import config_reader


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


class MatrixGenerator:
    def __init__(self, pol_sar_data: PolSARData, dir_path: str):
        self.pol_sar_data = pol_sar_data
        self.dir_path = dir_path

    def C_matrix_input(self):
        """
        Generate C-matrix from polarization data.
        :return:
        """
        if self.pol_sar_data.polar_type == FULL_POLARIZATION:
            channel_num = 3
        else:
            channel_num = 2
        shape, polar_type = config_reader(self.dir_path)
        matrix_set = []
        if polar_type != self.pol_sar_data.polar_type:
            raise ValueError("Polarization type error")
        for i in range(1, channel_num + 1):
            for j in range(1, channel_num + 1):
                if i == j:
                    file_path = os.path.join(self.dir_path, f'C{i}{j}.bin')
                    matrix = np.fromfile(file_path, dtype=np.float32)
                    matrix = matrix.reshape((shape[0], shape[1]))
                    matrix_set.append(matrix)
                if i < j:
                    real_path = os.path.join(self.dir_path, f'C{i}{j}_real.bin')
                    imag_path = os.path.join(self.dir_path, f'C{i}{j}_imag.bin')
                    real_data = np.fromfile(real_path, dtype=np.float32)
                    imag_data = np.fromfile(imag_path, dtype=np.float32)
                    real_data = real_data.reshape((shape[0], shape[1]))
                    imag_data = imag_data.reshape((shape[0], shape[1]))
                    matrix = real_data + 1j * imag_data
                    matrix_set.append(matrix)
                if i > j:
                    matrix_set.append(np.zeros(shape))
        C_matrix = np.dstack(matrix_set)
        if self.pol_sar_data.polar_type == FULL_POLARIZATION:
            C_matrix = C_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 3, 3)
        else:
            C_matrix = C_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
        self.pol_sar_data.set_C_matrix(C_matrix)

    def T_matrix_input(self):
        """
        Generate T-matrix from polarization data.
        :return:
        """
        if self.pol_sar_data.polar_type == FULL_POLARIZATION:
            channel_num = 3
        else:
            channel_num = 2
        shape, polar_type = config_reader(self.dir_path)
        matrix_set = []
        if polar_type != self.pol_sar_data.polar_type:
            raise ValueError("Polarization type error")
        for i in range(1, channel_num + 1):
            for j in range(1, channel_num + 1):
                if i == j:
                    file_path = os.path.join(self.dir_path, f'T{i}{j}.bin')
                    matrix = np.fromfile(file_path, dtype=np.float32)
                    matrix = matrix.reshape((shape[0], shape[1]))
                    matrix_set.append(matrix)
                if i < j:
                    real_path = os.path.join(self.dir_path, f'T{i}{j}_real.bin')
                    imag_path = os.path.join(self.dir_path, f'T{i}{j}_imag.bin')
                    real_data = np.fromfile(real_path, dtype=np.float32)
                    imag_data = np.fromfile(imag_path, dtype=np.float32)
                    real_data = real_data.reshape((shape[0], shape[1]))
                    imag_data = imag_data.reshape((shape[0], shape[1]))
                    matrix = real_data + 1j * imag_data
                    matrix_set.append(matrix)
                if i > j:
                    matrix_set.append(np.zeros(shape))
        T_matrix = np.dstack(matrix_set)
        if self.pol_sar_data.polar_type == FULL_POLARIZATION:
            T_matrix = T_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 3, 3)
        else:
            T_matrix = T_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
        self.pol_sar_data.set_T_matrix(T_matrix)






if __name__ == '__main__':
    # print(config_reader(
    #    'F:\lab\S1A_IW_SLC__1SDV_20180505T095436_20180505T095503_021768_025901_91B7\S1A_IW_SLC__1SDV_20180505T095436_20180505T095503_021768_025901_91B7.SAFE\IW2\IW2\C2\config.txt'))
    data = PolSARData('input_test', 5000, 5894, DUAL_POLARIZATION)
    generator = MatrixGenerator(data, r'F:\lab\PolSARpro数据\全极化T3\T3')
    # C_matrix_input(
    #     'F:\lab\S1A_IW_SLC__1SDV_20180505T095436_20180505T095503_021768_025901_91B7\S1A_IW_SLC__1SDV_20180505T095436_20180505T095503_021768_025901_91B7.SAFE\IW2\IW2\C2',
    #     data)
    # print(data.is_C_matrix_available())
    generator.T_matrix_input()
    print(data.is_T_matrix_available())
