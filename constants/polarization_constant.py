"""
    Constants related to the polarization.
"""

FULL_POLARIZATION = 'full'
DUAL_POLARIZATION = 'dual'

FULL_POLARIZATION_CHANNELS = ['HH', 'HV', 'VH', 'VV']
DUAL_POLARIZATION_CHANNELS = {'PP1': ['HH', 'HV'], 'PP2': ['VV', 'VH'], 'PP3': ['HH', 'VV']}

BIN_FULL_POLARIZATION_CHANNELS = ['s11', 's12', 's21', 's22']
BIN_DUAL_POLARIZATION_CHANNELS = [['s11', 's21'], ['s22', 's21'], ['s11', 's22']]
