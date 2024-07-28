"""
    A class for conducting process processes and other processes
"""
from model.pol_sar_data import PolSARData
from process.ps_decomposition_base import *
from process.ps_C_and_T_generator import *
from constants.polarization_constant import *
from file_reader import read_tiff_full_as_SAR, read_tiff_dual_as_SAR
from file_reader import read_dat_full_as_SAR, read_dat_dual_as_SAR
from file_reader import read_bin_full_as_SAR, read_bin_dual_as_SAR, read_T_bin_as_SAR
from util.file_discover import *


class WorkSteps:
    def __init__(self, proj_name):
        self.input_data = None
        self.proj_name = proj_name

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
        else:
            raise ValueError('file_type must be either "tiff" or "dat" or "bin"')
        self.input_data = PolSARData(self.proj_name, row, col, polar_type)
        self.input_data.set_S_matrix(matrix)

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
        generate = CandTGenerator(self.input_data, dir_path)
        if generate_type == C_GENERATE:
            # TODO:调用生成C矩阵的函数
            generate.C_matrix_input()
            join_file_name(C_GENERATE)
        if generate_type == T_GENERATE:
            # TODO:调用生成T矩阵的函数
            generate.T_matrix_input()
            join_file_name(T_GENERATE)

    def run_decomposition(self, decomposition_type, output_dir):
        """
        run the process
        :param decomposition_type: the type of the process constant, e.g. 'Yamaguchi4_Y4O'
        :param output_dir: the directory of the output files , defined by PolSARpro
        :return: output_file: file names of the process , sorted by channels
        """
        if not self.check_data():
            raise ValueError('Input data is not valid')
        decomposition = DecompositionBase(decomposition_type, output_dir)
        # TODO: 根据DECOMPOSITION_FUNCTION_DICT调用API
        output_file = decomposition.join_file_name()
        #decomposition.update_status()
        return decomposition.check_output_valid()


if __name__ == '__main__':
    workflow_tiff = WorkSteps('test1')
    workflow_tiff.read_data(TIFF_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat_tiff\C', 5000, 5894)
    print(workflow_tiff.check_data())
    workflow_dat = WorkSteps('test2')
    workflow_dat.read_data(DAT_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\dat\C', 5000, 5894)
    print(workflow_dat.check_data())
    workflow_bin = WorkSteps('test3')
    workflow_bin.read_data(BIN_FILE, FULL_POLARIZATION, r'F:\lab\Evaluation_Platform\file_reader\bin\full', 5000, 5894)
    print(workflow_bin.check_data())
    # TODO:T_BIN读入测试
