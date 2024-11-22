from constants.decomposition_constant import *
from constants.polarization_constant import *
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


if __name__ == '__main__':
    get_decomposition_details('Yamaguchi4_Y4O')
