from enum import Enum


class PolarizationType(Enum):
    FULL_POLARIZATION = 0
    DUAL_POLARIZATION = 1

    FULL_POLARIZATION_CHANNELS = ['HH', 'HV', 'VH', 'VV']
    DUAL_POLARIZATION_TYPES = ['PP1', 'PP2', 'PP3']
    PP1_CHANNELS = ['HH', 'HV']
    PP2_CHANNELS = ['VV', 'VH']
    PP3_CHANNELS = ['HH', 'VV']
