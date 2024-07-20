"""
    Constants related to the process process.
"""

from util.process_constant import get_decomposition_details

DECOMPOSITION_TYPES = ['Yamaguchi4_Y4O']

# process process status
PROCESSING = 'running'
FINISHED = 'finished'

DECOMPOSITION_FUNCTION_DICT = {'Yamaguchi4_Y4O': 'yamaguchi_4components_decomposition'}

'''
    Constants related to different process processes.
    Including channels,channel_suffix,visible_suffix
'''
Yamaguchi4_Y4O_dict = {'channels': {'Pd': '_Dbl', 'Pc': '_Hlx', 'Ps': '_Odd', 'Pv': '_Vol'},
                       'channel_suffix': ['.bin', '.bin.hdr', '_dB.bmp', '_dB.bmp.hdr'],
                       'visible_suffix': ['_RGB.bmp', '_RGB.bmp.hdr']}

if __name__ == '__main__':
    get_decomposition_details('Yamaguchi4_Y4O')
