"""
    Constants related to the polarization.
"""

FULL_POLARIZATION = 'full'
DUAL_POLARIZATION = 'dual'
TIFF_FILE = 'tiff'
DAT_FILE = 'dat'
BIN_FILE = 'bin'
T_BIN_FILE = 't_bin'

FULL_POLARIZATION_CHANNELS = ['HH', 'HV', 'VH', 'VV']
DUAL_POLARIZATION_CHANNELS = {'pp1': ['HH', 'HV'], 'pp2': ['VV', 'VH'], 'pp3': ['HH', 'VV']}

BIN_FULL_POLARIZATION_CHANNELS = ['s11', 's12', 's21', 's22']
BIN_DUAL_POLARIZATION_CHANNELS = {'pp1': ['s11', 's21'], 'pp2': ['s22', 's21'], 'pp3': ['s11', 's22']}

GENERATE_TYPES = ['C_Generate', 'T_Generate']
C_GENERATE = 'C_Generate'
T_GENERATE = 'T_Generate'

GENERATE_OUTPUT = {'mask_name': ['mask_valid_pixels.bin', 'mask_valid_pixels.bin.hdr',
                                 'mask_valid_pixels.bmp', 'mask_valid_pixels.bmp.hdr'],
                   'visible_name': ['RGB1.bmp', 'RGB1.bmp.hdr']
                   }
