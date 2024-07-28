# TODO:find all files from a proj folder
import os
import re
from constants.polarization_constant import *
from .file_name_reg import change_slash


def find_tiff_files(dir_path, polar_type, dual_type=None):
    files = os.listdir(dir_path)
    file_dict = {}
    if polar_type == FULL_POLARIZATION:
        for file in files:
            for channel in FULL_POLARIZATION_CHANNELS:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.tiff', file) is not None):
                    file_dict[channel] = file
    elif polar_type == DUAL_POLARIZATION and dual_type is not None:
        for file in files:
            for channel in DUAL_POLARIZATION_CHANNELS[dual_type]:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.tiff', file) is not None):
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
                        re.search('\.dat', file) is not None):
                    file_dict[channel] = file
    elif polar_type == DUAL_POLARIZATION and dual_type is not None:
        for file in files:
            for channel in DUAL_POLARIZATION_CHANNELS[dual_type]:
                if (re.search(f'[^a-zA-Z0-9]{channel}[^a-zA-Z0-9]', file) is not None and
                        re.search('\.dat', file) is not None):
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


if __name__ == '__main__':
    find_tiff_files('F:\lab\Evaluation_Platform\\file_reader\dat_tiff\C', FULL_POLARIZATION)
    find_dat_files('F:\lab\Evaluation_Platform\\file_reader\dat\C', FULL_POLARIZATION)
    #match = re.search('[^a-zA-Z0-9](HH)[^a-zA-Z0-9]', '1144_010_C_HH_L1A.tiff')
    #print(match.group(1))
