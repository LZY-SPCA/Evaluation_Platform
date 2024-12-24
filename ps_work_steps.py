"""
    A class for conducting process processes and other processes
"""
import os.path

from constants.decomposition_constant import SOFT_PATH, DECOMPOSITION_FUNCTION_DICT
from eval_api.PolSARpro import PolSARpro
from process.ps_decomposition_base import *
from file_reader.ps_matrix_input import *
from file_reader import read_tiff_full_as_SAR, read_tiff_dual_as_SAR
from file_reader import read_dat_full_as_SAR, read_dat_dual_as_SAR
from file_reader import read_bin_full_as_SAR, read_bin_dual_as_SAR, read_T_bin_as_SAR, read_S_bin_as_SAR
from util.constant_process import process_input_output_format, process_element_files, check_output_valid, \
    process_corr_files
from util.file_discover import *

from pathlib import Path


class WorkSteps:
    def __init__(self, proj_name, input_dir, output_dir, row=None, col=None, polar_type=None):
        self.PolSARpro = None
        self.proj_name = proj_name
        self.input_dir = input_dir
        # TODO：统一管理config_read,等候删除后续部分
        if config_valid(input_dir):
            self.row, self.col, self.polar_type = config_reader(input_dir)
        else:
            if row is None or col is None or polar_type is None:
                raise ValueError("When config is unavailable, Please provide either row or col or polar type")
            self.row = row
            self.col = col
            self.polar_type = polar_type
        self.input_data = PolSARData(proj_name, self.row, self.col, self.polar_type)
        self.output_dir = output_dir
        self.soft_path = os.path.join(os.path.dirname(Path(__file__).resolve()), SOFT_PATH)

    def read_data(self, file_type, polar_type, dir_path, row: int, col: int, dual_type=None):
        """
        Call the functions in file_reader package to read the data from file
        :param file_type: type of the file e.g. bin,dat,tiff,t_bin
        :param polar_type: type of polarization e.g. full,dual
        :param dir_path: path of the directory
        :param dual_type: type of dual e.g. 'pp1' , not use when polar_type is full
        :param row: row of the data matrix , not use when file_type is tiff
        :param col: column of the data matrix , not use when file_type is tiff
        :return:
        """
        self.input_dir = dir_path
        if config_valid(dir_path):
            row, col, polar_type = config_reader(dir_path)
        if file_type == TIFF_FILE:
            tiff_dict = find_tiff_files(dir_path, polar_type, dual_type)
            if polar_type == FULL_POLARIZATION:
                matrix = read_tiff_full_as_SAR(dir_path, tiff_dict, row, col)
            elif polar_type == DUAL_POLARIZATION:
                matrix = read_tiff_dual_as_SAR(dir_path, tiff_dict, row, col, dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        elif file_type == DAT_FILE:
            dat_fict = find_dat_files(dir_path, polar_type, dual_type)
            if polar_type == FULL_POLARIZATION:
                matrix = read_dat_full_as_SAR(dir_path, dat_fict, row, col)
            elif polar_type == DUAL_POLARIZATION:
                matrix = read_dat_dual_as_SAR(dir_path, dat_fict, row, col, dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        elif file_type == BIN_FILE:
            real_dict, imag_dict = find_bin_files(dir_path, polar_type, dual_type)
            if polar_type == FULL_POLARIZATION:
                matrix = read_bin_full_as_SAR(dir_path, real_dict, imag_dict, row, col)
            elif polar_type == DUAL_POLARIZATION:
                matrix = read_bin_dual_as_SAR(dir_path, real_dict, imag_dict, row, col, dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        elif file_type == T_BIN_FILE:
            # 对应pol_format为T3
            matrix = read_T_bin_as_SAR(row, col, dir_path, polar_type)
            self.input_data = PolSARData(self.proj_name, matrix.shape[0], matrix.shape[1], polar_type)
            self.input_data.set_T_matrix(matrix)
            return
        elif file_type == S_BIN_FILE:
            # 该类型的S矩阵不区分实部和虚部，对应pol_format为S2
            matrix = read_S_bin_as_SAR(row, col, dir_path, polar_type)
        else:
            raise ValueError('file_type must be either "tiff" or "dat" or "bin"')
        self.input_data = PolSARData(self.proj_name, row, col, polar_type)
        self.input_data.set_S_matrix(matrix)

    def read_pol_sar_data(self, input_path, pol_format):
        reader_func = globals()[f'{pol_format}_matrix_input'](input_path, self.input_data)

    def init_polsarpro(self, pol_format):
        """
        初始化PolSARpro执行类
        :return:
        """
        self.PolSARpro = PolSARpro(soft_path=self.soft_path, input_dir=self.input_dir, output_dir=self.output_dir,
                                   pol_format=pol_format,
                                   row_offset=0, row_final=self.input_data.height, col_offset=0,
                                   col_final=self.input_data.width)

    def check_data(self):
        """
        check whether the PolSARData is valid
        :return:
        """
        if self.input_data is not None:
            if self.input_data.is_S_matrix_available() or self.input_data.is_T_matrix_available():
                return True
        return False

    def generate_matrix(self, dir_path, generate_type):
        file = None
        if generate_type == S_GENERATE:
            # TODO：调用提取S矩阵及可视化的函数
            file = join_file_name(S_GENERATE)
        if generate_type == C_GENERATE:
            # TODO:调用生成C矩阵及可视化的函数
            C3_matrix_input(dir_path, self.input_data)
            file = join_file_name(C_GENERATE)
        if generate_type == T_GENERATE:
            # TODO:调用生成T矩阵及可视化的函数
            T3_matrix_input(dir_path, self.input_data)
            file = join_file_name(T_GENERATE)
        return file

    def run_filter(self, process_type, **kwargs):
        """
            对于有input_output_format参数的处理（如滤波）
            其他处理可能不存在该字段，故分开
            需要修改输入路径
            该函数同样负责orientation_compensation的调用
        :param process_type:
        :param kwargs:
        :return:
        """
        process_func = getattr(self.PolSARpro, FILTER_FUNCTION_DICT[process_type])
        process_func(**kwargs)
        output_format = self.PolSARpro.pol_format
        if 'input_output_format' in kwargs:
            output_format = process_input_output_format(kwargs['input_output_format'])
        output_dir = process_output_dir(process_type, self.input_dir, output_format)
        self.input_dir = output_dir
        self.output_dir = output_dir
        try:
            self.read_pol_sar_data(output_dir, output_format)
        except Exception as e:
            print(str(e))
            return False
        return True

    def run_decomposition(self, decomposition_type, **kwargs):
        """
        run the process
        :param decomposition_type: the type of the process constant, e.g. 'Yamaguchi4_Y4O'
        :return: output_file: file names of the process , sorted by channels
        """
        if not self.check_data():
            raise ValueError('Input data is valid')
        decomposition = DecompositionBase(decomposition_type, self.output_dir)
        decomposition_func = getattr(self.PolSARpro, DECOMPOSITION_FUNCTION_DICT[decomposition_type])
        decomposition_func(**kwargs)
        return decomposition.check_output_valid()

    def run_process_element(self, **kwargs):
        element_process_dict = kwargs['element_process_dict']
        for (element_index, process_format) in element_process_dict.items():
            if process_format == 'None':
                continue
            self.PolSARpro.process_elements(element_index, process_format)
        files = process_element_files(self.output_dir, self.PolSARpro.pol_format, element_process_dict)
        return check_output_valid(files)

    def run_process_corr(self, **kwargs):
        element_index_list = kwargs['element_index_list']
        window_size_row = kwargs['window_size_row']
        window_size_col = kwargs['window_size_col']
        for element_index in element_index_list:
            self.PolSARpro.process_corr(element_index=element_index, window_size_row=window_size_row,
                                        window_size_col=window_size_col)
        files = process_corr_files(self.output_dir)
        return check_output_valid(files)

    def run_detection(self):
        pass

    def run_recognition(self):
        pass

    """
        def create_pauli_rgb_file(self, input_dir, output_file, min_max_auto, blue_min, blue_max, red_min, red_max, green_min, green_max):
    """
    def run_visible(self, suffix='origin'):
        file_name = 'PauliRGB_' + suffix + '.bmp'
        visible_file_path = os.path.join(self.output_dir, file_name)
        self.PolSARpro.create_pauli_rgb_file(input_dir=self.input_dir, output_file=visible_file_path, min_max_auto=1,
                                             blue_min=0, blue_max=0, red_min=0, red_max=0, green_min=0, green_max=0)
        file_dict = {'visible': [visible_file_path]}
        if suffix == 'orientation_compensation':
            file_dict['compensation'] = [(os.path.join(self.output_dir, 'orientation_estimation.bmp'))]
        return check_output_valid(file_dict)


if __name__ == '__main__':
    # workflow_tiff = WorkSteps('test1')
    # workflow_tiff.read_data(TIFF_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat_tiff\C', 5000,
    #                         5894)
    # print(workflow_tiff.check_data())
    # workflow_dat = WorkSteps('test2')
    # workflow_dat.read_data(DAT_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat\C', 5000, 5894)
    # print(workflow_dat.check_data())
    # workflow_bin = WorkSteps('test3')
    # workflow_bin.read_data(BIN_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\bin\full', 5000, 5894)
    # print(workflow_bin.check_data())
    # workflow_T_bin = WorkSteps('test4')
    # workflow_T_bin.read_data(T_BIN_FILE, FULL_POLARIZATION,r'F:\lab\Evaluation_Platform\全极化T3\T3', 5000, 5894)
    # print(workflow_T_bin.check_data())
    # workflow_S_bin = WorkSteps('test5')
    # workflow_S_bin.read_data(S_BIN_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\全极化S2\S2', 5000, 5894)
    # print(workflow_S_bin.check_data())
    # print(workflow_S_bin.soft_path)

    pol_sar_data = PolSARData('111', 5000, 5894, 'full')
    pol_format = 'T3'
    reader_func = globals()[f'{pol_format}_matrix_input']('F:\lab\Evaluation_Platform\全极化T3\T3', pol_sar_data)
