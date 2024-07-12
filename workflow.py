"""
    A class for conducting decomposition processes and other processes
"""
from model.pol_sar_data import PolSARData
from decomposition.decomposition_base import *
from file_reader import read_tiff_full_as_SAR, read_tiff_dual_as_SAR
from file_reader import read_dat_full_as_SAR, read_dat_dual_as_SAR
from file_reader import read_bin_full_as_SAR, read_bin_dual_as_SAR


class Workflow:
    def __init__(self, proj_name):
        self.input_data = None
        self.proj_name = proj_name

    def read_data(self, file_type, polar_type, file_path, file_name, dual_type, row: int, col: int):
        """
        Call the functions in file_reader package to read the data from file
        :param file_type: type of the file e.g. bin,dat,tiff
        :param polar_type: type of polarization e.g. full,dual
        :param file_path: path of the file
        :param file_name: name of the file
        :param dual_type: type of dual e.g. 'PP1' , not use when polar_type is full
        :param row: row of the data matrix , not use when file_type is tiff
        :param col: column of the data matrix , not use when file_type is tiff
        :return:
        """
        if file_type == 'tiff':
            if polar_type == 'full':
                self.input_data = read_tiff_full_as_SAR(file_path, file_name)
            elif polar_type == 'dual':
                self.input_data = read_tiff_dual_as_SAR(dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        elif file_type == 'dat':
            if polar_type == 'full':
                self.input_data = read_dat_full_as_SAR(row, col)
            elif polar_type == 'dual':
                self.input_data = read_dat_dual_as_SAR(row, col, dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        elif file_type == 'bin':
            if polar_type == 'full':
                self.input_data = read_bin_full_as_SAR(row, col)
            elif polar_type == 'dual':
                self.input_data = read_bin_dual_as_SAR(row, col, dual_type)
            else:
                raise ValueError('polar_type must be either "full" or "dual"')
        else:
            raise ValueError('file_type must be either "tiff" or "dat" or "bin"')

    def check_data(self):
        """
        check whether the PolSARData is valid
        :return:
        """
        if self.input_data is not None:
            if self.input_data.is_S_matrix_available() or self.input_data.is_T_matrix_unavailable():
                return True
        return False

    def run_decomposition(self, decomposition_type, output_dir, status):
        """
        run the decomposition
        :param decomposition_type: the type of the decomposition constant, e.g. 'Yamaguchi4_Y4O'
        :param output_dir: the directory of the output files , defined by PolSARpro
        :param status: status of the decomposition process, either 'running' or 'finished'
        :return: output_file: file names of the decomposition , sorted by channels
        """
        if not self.check_data():
            raise ValueError('Input data is not valid')
        decomposition = DecompositionBase(decomposition_type, output_dir, status)
        # TODO: 调用API
        output_file = decomposition.join_file_name()
        return output_file
