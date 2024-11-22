# TODO:find all files from a proj folder
import os
import re

import numpy as np

from constants.polarization_constant import *
from util.constant_process import get_generate_details
from .file_name_reg import change_slash


def find_tiff_files(dir_path, polar_type, dual_type=None):
    files = os.listdir(dir_path)
    file_dict = {}
    if polar_type == FULL_POLARIZATION:
        for file in files:
            for channel in FULL_POLARIZATION_CHANNELS:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.tiff$', file) is not None):
                    file_dict[channel] = file
    elif polar_type == DUAL_POLARIZATION and dual_type is not None:
        for file in files:
            for channel in DUAL_POLARIZATION_CHANNELS[dual_type]:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.tiff$', file) is not None):
                    file_dict[channel] = file
    print(file_dict)
    return file_dict


def find_dat_files(dir_path, polar_type, dual_type=None):
    files = os.listdir(dir_path)
    file_dict = {}
    if polar_type == FULL_POLARIZATION:
        for file in files:
            for channel in FULL_POLARIZATION_CHANNELS:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.dat$', file) is not None):
                    file_dict[channel] = file
    elif polar_type == DUAL_POLARIZATION and dual_type is not None:
        for file in files:
            for channel in DUAL_POLARIZATION_CHANNELS[dual_type]:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.dat$', file) is not None):
                    file_dict[channel] = file
    print(file_dict)
    return file_dict


def find_bin_files(dir_path, polar_type, dual_type=None):
    files = os.listdir(dir_path)
    real_file_dict = {}
    imag_file_dict = {}
    if polar_type == FULL_POLARIZATION:
        for file in files:
            for name in BIN_FULL_POLARIZATION_CHANNELS:
                if re.search(f'{name}_real.bin', file) is not None:
                    real_file_dict[name] = file
                if re.search(f'{name}_imag.bin', file) is not None:
                    imag_file_dict[name] = file
    elif polar_type == DUAL_POLARIZATION and dual_type is not None:
        for file in files:
            for name in BIN_DUAL_POLARIZATION_CHANNELS[dual_type]:
                if re.search(f'{name}_real.bin', file) is not None:
                    real_file_dict[name] = file
                if re.search(f'{name}_imag.bin', file) is not None:
                    imag_file_dict[name] = file
    print(real_file_dict)
    print(imag_file_dict)
    return real_file_dict, imag_file_dict


def config_reader(config_dir):
    """
    C矩阵和T矩阵的直接读入依赖PolSARpro生成的config.txt
    :return:
    """
    row = 0
    col = 0
    polar_type = None
    config_path = os.path.join(config_dir, 'config.txt')
    try:
        config_file = open(config_path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError('Config file not found')
    row_flag = False
    col_flag = False
    polar_flag = False
    for line in config_file:
        if line.rstrip('\n') == 'Nrow':
            row_flag = True
            continue
        if row_flag:
            row_flag = False
            row = int(line.rstrip('\n'))
            continue
        if line.rstrip('\n') == 'Ncol':
            col_flag = True
            continue
        if col_flag:
            col_flag = False
            col = int(line.rstrip('\n'))
            continue
        if line.rstrip('\n') == 'PolarType':
            polar_flag = True
            continue
        if polar_flag:
            polar_flag = False
            read_type = line.rstrip('\n')
            if read_type == FULL_POLARIZATION:
                polar_type = FULL_POLARIZATION
            elif read_type == DUAL_POLARIZATION:
                polar_type = DUAL_POLARIZATION
            else:
                raise ValueError('PolarType not supported')
            break
    if row == 0 or col == 0:
        raise Exception('row or col not found')
    return row, col, polar_type

def config_valid(config_path):
    config_name = os.path.join(config_path, 'config.txt')
    row_flag = False
    col_flag = False
    type_flag = False
    try:
        config_file = open(config_name, 'r')
    except FileNotFoundError:
        return False
    for line in config_file:
        if line.rstrip('\n') == 'Nrow':
            row_flag = True
        if line.rstrip('\n') == 'Ncol':
            col_flag = True
        if line.rstrip('\n') == 'PolarType':
            type_flag = True
    return row_flag and col_flag and type_flag


if __name__ == '__main__':
    find_tiff_files('F:\lab\Evaluation_Platform\\file_reader\dat_tiff\C', FULL_POLARIZATION)
    find_dat_files('F:\lab\Evaluation_Platform\\file_reader\dat\C', FULL_POLARIZATION)
    #match = re.search('[^a-zA-Z0-9](HH)[^a-zA-Z0-9]', '1144_010_C_HH_L1A.tiff')
    #print(match.group(1))
