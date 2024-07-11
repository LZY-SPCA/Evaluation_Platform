from model.decomposition_output import DecompositionOutput

DECOMPOSITION_TYPES = ['Yamaguchi4_Y4O']

# decomposition process status
PROCESSING = 'processing'
FINISHED = 'finished'

Yamaguchi4_Y4O_dict = {'channels': {'Pd': '_Dbl', 'Pc': '_Hlx', 'Ps': '_Odd', 'Pv': '_Vol'},
                       'channel_suffix': ['.bin', '.bin.hdr', '_dB.bmp', '_dB.bmp.hdr'],
                       'visible_suffix': ['_RGB.bmp', '_RGB.bmp.hdr']}


def get_details(decomposition_type) -> DecompositionOutput:
    if decomposition_type in DECOMPOSITION_TYPES:
        type_dict = eval(f'{decomposition_type}_dict')
        print(type_dict)
        channel_name = type_dict['channels']
        channel_suffix = type_dict['channel_suffix']
        visible_suffix = type_dict['visible_suffix']
        output = DecompositionOutput(channel_name,
                                     channel_suffix,
                                     visible_suffix)
        return output


if __name__ == '__main__':
    get_details('Yamaguchi4_Y4O')
