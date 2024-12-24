import os

from constants.polarization_constant import *
from ps_work_steps import WorkSteps
from util.file_discover import config_valid


def data_input_api(input_dir, output_dir, pol_format, row=None, col=None, polar_type=None):
    ws = WorkSteps('proj_name', input_dir, output_dir, row, col, polar_type)
    # ws.read_data(file_type, polar_type, input_dir, row, col, dual_type)
    ws.read_pol_sar_data(input_dir, pol_format)
    ws.init_polsarpro(pol_format)
    return ws


def data_check_valid_api(ws):
    return ws.check_data()


def filter_api(ws: WorkSteps, process_type, **kwargs):
    return ws.run_filter(process_type, **kwargs)


def decomposition_api(ws: WorkSteps, decomposition_type, **kwargs):
    res = ws.run_decomposition(decomposition_type, **kwargs)
    return res


def process_element_api(ws: WorkSteps, **kwargs):
    return ws.run_process_element(**kwargs)


def process_corr_api(ws: WorkSteps, **kwargs):
    return ws.run_process_corr(**kwargs)


def orientation_compensation_api(ws: WorkSteps, **kwargs):
    return ws.run_filter('orientation_compensation', **kwargs)


def basis_change_api(ws: WorkSteps, **kwargs):
    return ws.run_filter('basis_change', **kwargs)


def create_visible_api(ws: WorkSteps, suffix=None):
    if suffix is None:
        return ws.run_visible()
    else:
        return ws.run_visible(suffix)


def config_valid_api(config_path):
    return config_valid(config_path)


if __name__ == '__main__':
    ws = data_input_api('F:\lab\Evaluation_Platform\全极化T3\T3', 'bin', 'F:\lab\Evaluation_Platform\全极化T3\T3', 'T3')
    print(ws.input_data.is_T_matrix_available())

    ws = data_input_api(r'F:\lab\Evaluation_Platform\full S2\S2', 'bin', r'F:\lab\Evaluation_Platform\full S2\S2', 'S2')
    print(ws.input_data.is_S_matrix_available())
