import os

from constants.decomposition_constant import *
from constants.polarization_constant import *
from constants.process_constant import *
from constants.filter_constant import INPUT_OUTPUT_FORMATS_DICT
from model.ps_decomposition_output import DecompositionOutput
from model.ps_generation_output import GenerationOutput


def get_decomposition_details(input_type) -> DecompositionOutput:
    """
    Transform process const dict into process output.
    :param input_type: the type of the process constant, e.g. 'Yamaguchi4_Y4O'
    :return: DecompositionOutput
    """
    if input_type in DECOMPOSITION_TYPES:
        type_dict = eval(f'{input_type}_dict')
        print(type_dict)
        if 'channels' in type_dict.keys():
            channel_name = type_dict['channels']
        else:
            channel_name = None
        if 'channel_suffix' in type_dict.keys():
            channel_suffix = type_dict['channel_suffix']
        else:
            channel_suffix = None
        if 'visible' in type_dict.keys():
            visible = type_dict['visible']
        else:
            visible = None
        if 'mask_suffix' in type_dict.keys():
            mask_suffix = type_dict['mask_suffix']
        else:
            mask_suffix = None
        output = DecompositionOutput(channel_name,
                                     channel_suffix,
                                     visible,
                                     mask_suffix)
        return output


def get_generate_details(input_type) -> GenerationOutput:
    if input_type in GENERATE_TYPES:
        type_dict = GENERATE_OUTPUT
        if 'visible_name' in type_dict.keys():
            visible_name = type_dict['visible_name']
        else:
            visible_name = None
        if 'mask_name' in type_dict.keys():
            mask_name = type_dict['mask_name']
        else:
            mask_name = None
        output = GenerationOutput(visible_name, mask_name)
        return output


def process_input_output_format(input_output_format):
    if input_output_format not in INPUT_OUTPUT_FORMATS_DICT.keys():
        raise ValueError(f'Input output format {input_output_format} not supported')
    if INPUT_OUTPUT_FORMATS_DICT[input_output_format] == 'change':
        new_format = input_output_format[-2:]
    else:
        new_format = input_output_format
    return new_format


def process_element_files(output_path, pol_format, element_process_dict):
    constant_dict = globals()[f'PROCESS_ELEMENTS_{pol_format}_OUTPUT']
    channel_dict = constant_dict['channels']
    channel_suffix_list = constant_dict['channel_suffix']
    file_dict = {}
    for (element_index, process_format) in element_process_dict.items():
        file_dict[element_index] = []
        for channel_suffix in channel_suffix_list:
            file_dict[element_index].append(os.path.join(output_path, (channel_dict[process_format].format(index=element_index) + channel_suffix)))
    return file_dict


def process_corr_files(output_path):
    constant_dict = globals()['PROCESS_CORR_OUTPUT']
    channel_dict = constant_dict['channels']
    channel_suffix_list = constant_dict['channel_suffix']
    file_dict = {}
    for (channel, file) in channel_dict.items():
        file_dict[channel] = []
        for channel_suffix in channel_suffix_list:
            file_dict[channel].append(os.path.join(output_path, (file+channel_suffix)))
    return file_dict



def check_output_valid(input_files):
    """
    检查输出文件是否有效（是否生成输出文件）
    合法输入：{'{channel_name}:[file_list]'}
    :return:
    """
    file_dict = input_files
    for f_list in file_dict.values():
        if type(f_list) is dict:
            for f_name in f_list:
                if not os.path.exists(f_name):
                    f_list.remove(f_name)
        else:
            for f_name in f_list[:]:
                if not os.path.exists(f_name):
                    f_list.remove(f_name)
    for key in list(file_dict.keys()):
        if len(file_dict[key]) == 0:
            del file_dict[key]
    return file_dict


if __name__ == '__main__':
    get_decomposition_details('Yamaguchi4_Y4O')
    print(process_input_output_format("S2C4"))
    print(process_input_output_format("T3"))
    print(process_element_files('F:\lab\Wuhan\T3', "T3",
                                {'11': 'mod', '12': 'db', '13': 'pha', '21': 'mod', '22': 'db', '23': 'pha',
                                  '31': 'mod', '32': 'db', '33': 'db'}))
    print(process_element_files('F:\lab\Wuhan\T3', "C3",
                                {'11': 'mod', '12': 'db', '13': 'pha', '21': 'mod', '22': 'db', '23': 'pha',
                                  '31': 'mod', '32': 'db', '33': 'db'}))
    print(process_element_files('F:\lab\Wuhan\T3', "S2", {'11': 'A', '12': 'Adb', '21': 'I', '22': 'pha'}))
    print(process_corr_files('F:\lab\Wuhan\T3'))
