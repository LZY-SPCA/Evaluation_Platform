"""
    Constants related to the process.
"""


DECOMPOSITION_TYPES = ['Yamaguchi4_Y4O', 'H_A_ALPHA', 'Cloude', 'Krogager', 'Huynen']

# process process status
PROCESSING = 'running'
FINISHED = 'finished'

SOFT_PATH = r'PolSARpro_bin\bin'

DECOMPOSITION_FUNCTION_DICT = {'Yamaguchi4_Y4O': 'yamaguchi_4components_decomposition', 'H_A_ALPHA': 'h_a_alpha_decomposition',
                               'Cloude': 'cloude_decomposition', 'Krogager': 'krogager_decomposition', 'Huynen': 'huynen_decomposition'}

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

Krogager_dict = {'channels': {'Ks': 'Krogager_Ks', 'Kd': 'Krogager_Kd', 'Kh': 'Krogager_Kh', 'Teta': 'Krogager_Teta'},
                 'channel_suffix': ['.bin', '_dB.bmp'],
                 'visible': ['Krogager_RGB.bmp']
                 }

Huynen_dict = {'channels': {'Huynen_C11': 'Huynen_C11_dB', 'Huynen_C22': 'Huynen_C22_dB', 'Huynen_C33': 'Huynen_C33_dB',
                            'Huynen_T11': 'Huynen_T11_dB', 'Huynen_T22': 'Huynen_T22_dB', 'Huynen_T33': 'Huynen_T33_dB'},
               'channel_suffix': ['.bmp'],
               'visible': ['Huynen_RGB.bmp']
               }

