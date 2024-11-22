import os

from constants.polarization_constant import *
from ps_work_steps import WorkSteps
from util.file_discover import config_valid


def data_input_api(input_dir, file_type, polar_type, row, col, output_dir, pol_format, dual_type=None):
    ws = WorkSteps('proj_name', input_dir, output_dir)
    ws.read_data(file_type, polar_type, input_dir, row, col, dual_type)
    ws.init_polsarpro(pol_format)
    return ws


def data_check_valid_api(ws):
    return ws.check_data()


def process_api(ws: WorkSteps, process_type, output_dir):
    ws.run_process(process_type, output_dir)


def decomposition_api(ws: WorkSteps, decomposition_type, **kwargs):
    res = ws.run_decomposition(decomposition_type, **kwargs)
    return res


def config_valid_api(config_path):
    return config_valid(config_path)

if __name__ == '__main__':
    data_input_api('F:/lab/Evaluation_Platform/file_reader/dat_tiff/C', 'tiff', 'full', 5000, 5894, 'pp1')
