"""
    Constants related to the process.
"""


DECOMPOSITION_TYPES = ['Yamaguchi4_Y4O', 'H_A_ALPHA']

# process process status
PROCESSING = 'running'
FINISHED = 'finished'

SOFT_PATH = r'PolSARpro_bin\bin'

DECOMPOSITION_FUNCTION_DICT = {'Yamaguchi4_Y4O': 'yamaguchi_4components_decomposition', 'H_A_ALPHA': 'h_a_alpha_decomposition',
                               'Cloude': 'cloude_decomposition'}

'''
    Constants related to different process.
    Including channels,channel_suffix,visible_suffix
    Dict name should be type名+_dict
'''
Yamaguchi4_Y4O_dict = {'channels': {'Pd': 'Yamaguchi4_Y4O_Dbl', 'Pc': 'Yamaguchi4_Y4O_Hlx', 'Ps': 'Yamaguchi4_Y4O_Odd', 'Pv': 'Yamaguchi4_Y4O_Vol'},
                       'channel_suffix': ['.bin', '.bin.hdr', '_dB.bmp', '_dB.bmp.hdr'],
                       'visible': ['Yamaguchi4_Y4O_RGB.bmp']}

H_A_ALPHA_dict = {'channels': {'alpha': 'alpha', 'beta': 'beta', 'delta': 'delta', 'gamma': 'gamma', 'lambda': 'lambda',
                               'entropy': 'entropy', 'anisotropy': 'anisotropy_db',
                               'combination_HA': 'combination_HA', 'combination_1mHA': 'combination_1mHA', 'combination_H1mA': 'combination_H1mA',
                               'combination_1mH1mA': 'combination_1mH1mA'},
                  'channel_suffix': ['.bmp', '.bin']
                  }

Cloude_dict = {'channels': {'Cloude_T11': 'Cloude_T11_dB', 'Cloude_T22': 'Cloude_T22_dB', 'Cloude_T33': 'Cloude_T33_dB'},
               'channel_suffix': ['.bmp'],
               'visible': ['Cloude_RGB.bmp']
               }

