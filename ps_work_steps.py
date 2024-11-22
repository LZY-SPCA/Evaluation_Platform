"""
    A class for conducting process processes and other processes
"""
import os.path

from constants.decomposition_constant import SOFT_PATH, DECOMPOSITION_FUNCTION_DICT
from eval_api.PolSARpro import PolSARpro
from model.pol_sar_data import PolSARData
from process.ps_decomposition_base import *
from process.ps_matrix_generator import *
from constants.polarization_constant import *
from file_reader import read_tiff_full_as_SAR, read_tiff_dual_as_SAR
from file_reader import read_dat_full_as_SAR, read_dat_dual_as_SAR
from file_reader import read_bin_full_as_SAR, read_bin_dual_as_SAR, read_T_bin_as_SAR, read_S_bin_as_SAR
from util.file_discover import *

from pathlib import Path

class WorkSteps:
    def __init__(self, proj_name, input_dir, output_dir):
        self.PolSARpro = None
        self.input_data = None
        self.proj_name = proj_name
        self.input_dir = input_dir
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
            matrix = read_T_bin_as_SAR(row, col, dir_path, polar_type)
            self.input_data = PolSARData(self.proj_name, matrix.shape[0], matrix.shape[1], polar_type)
            self.input_data.set_T_matrix(matrix)
            return
        elif file_type == S_BIN_FILE:
            matrix = read_S_bin_as_SAR(row, col, dir_path, polar_type)
        else:
            raise ValueError('file_type must be either "tiff" or "dat" or "bin"')
        self.input_data = PolSARData(self.proj_name, row, col, polar_type)
        self.input_data.set_S_matrix(matrix)

    def init_polsarpro(self, pol_format):
        """
        初始化PolSARpro执行类
        :return:
        """
        self.PolSARpro = PolSARpro(soft_path=self.soft_path, input_dir=self.input_dir, output_dir=self.output_dir, pol_format=pol_format,
                                   row_offset=0, row_final=self.input_data.height, col_offset=0, col_final=self.input_data.width)

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
        generate = MatrixGenerator(self.input_data, dir_path)
        file = None
        if generate_type == S_GENERATE:
            # TODO：调用提取S矩阵及可视化的函数
            file = join_file_name(S_GENERATE)
        if generate_type == C_GENERATE:
            # TODO:调用生成C矩阵及可视化的函数
            generate.C_matrix_input()
            file = join_file_name(C_GENERATE)
        if generate_type == T_GENERATE:
            # TODO:调用生成T矩阵及可视化的函数
            generate.T_matrix_input()
            file = join_file_name(T_GENERATE)
        return file

    def run_process(self, process_type, dir_path):
        if self.input_data.T_matrix_valid() or self.input_data.C_matrix_valid():
            # TODO:调用processAPI
            generate = MatrixGenerator(self.input_data, dir_path)
            if self.input_data.T_matrix_valid():
                generate.T_matrix_input()
            elif self.input_data.C_matrix_valid():
                generate.C_matrix_input()

    def run_decomposition(self, decomposition_type, **kwargs):
        """
        run the process
        :param decomposition_type: the type of the process constant, e.g. 'Yamaguchi4_Y4O'
        :param output_dir: the directory of the output files , defined by PolSARpro
        :return: output_file: file names of the process , sorted by channels
        """
        if not self.check_data():
            raise ValueError('Input data is valid')
        decomposition = DecompositionBase(decomposition_type, self.output_dir)
        decomposition_func = getattr(self.PolSARpro, DECOMPOSITION_FUNCTION_DICT[decomposition_type])
        decomposition_func(**kwargs)
        # TODO: 根据DECOMPOSITION_FUNCTION_DICT调用API
        output_file = decomposition.join_file_name()
        #decomposition.update_status()
        return decomposition.check_output_valid()

    def run_detection(self):
        pass

    def run_recognition(self):
        pass


if __name__ == '__main__':
    workflow_tiff = WorkSteps('test1')
    workflow_tiff.read_data(TIFF_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat_tiff\C', 5000,
                            5894)
    print(workflow_tiff.check_data())
    workflow_dat = WorkSteps('test2')
    workflow_dat.read_data(DAT_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat\C', 5000, 5894)
    print(workflow_dat.check_data())
    workflow_bin = WorkSteps('test3')
    workflow_bin.read_data(BIN_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\bin\full', 5000, 5894)
    print(workflow_bin.check_data())
    workflow_T_bin = WorkSteps('test4')
    workflow_T_bin.read_data(T_BIN_FILE, FULL_POLARIZATION,r'F:\lab\Evaluation_Platform\全极化T3\T3', 5000, 5894)
    print(workflow_T_bin.check_data())
    workflow_S_bin = WorkSteps('test5')
    workflow_S_bin.read_data(S_BIN_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\全极化S2\S2', 5000, 5894)
    print(workflow_S_bin.check_data())
    print(workflow_S_bin.soft_path)
