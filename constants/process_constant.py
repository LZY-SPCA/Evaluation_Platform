PROCESS_ELEMENTS_S2_OUTPUT = {
    'channels': {'A': 'A{index}', 'Adb': 'I{index}_db', 'I': 'I{index}', 'pha': 'S{index}_pha'},
    'channel_suffix': ['.bmp']
    }

PROCESS_ELEMENTS_T3_OUTPUT = {'channels': {'mod': 'T{index}_mod', 'db': 'T{index}_db', 'pha': 'T{index}_pha'},
                              'channel_suffix': ['.bmp'],
                              }

PROCESS_ELEMENTS_C3_OUTPUT = {'channels': {'mod': 'C{index}_mod', 'db': 'C{index}_db', 'pha': 'C{index}_pha'},
                              'channel_suffix': ['.bmp'],
                              }

PROCESS_CORR_OUTPUT = {'channels': {'Ro12': 'Ro13', 'Ro13': 'Ro13', 'Ro23': 'Ro23'},
                       'channel_suffix': ['_mod.bmp', '_pha.bmp']}
