from constants.polarization_constant import *
from ps_work_steps import WorkSteps


def data_input_api(dir_path, file_type, polar_type, row, col, dual_type=None):
    ws = WorkSteps('proj_name')
    ws.read_data(file_type, polar_type, dir_path, row, col, dual_type)
    return ws


def data_check_valid(ws):
    return ws.check_data()


def decomposition_api(ws: WorkSteps, decomposition_type, output_dir):
    res = ws.run_decomposition(decomposition_type, output_dir)
    return res


if __name__ == '__main__':
    data_input_api('F:/lab/Evaluation_Platform/file_reader/dat_tiff/C', 'tiff', 'full', 5000, 5894, 'pp1')
