"""
    保存了与filter以及类filter调用的相关constant
"""

FILTER_NAME = ['an_yang', 'lee_refined']

FILTER_FUNCTION_DICT = {'an_yang': 'an_yang_filter', 'lee_refined': 'lee_refined_filter', 'orientation_compensation': 'orientation_compensation', 'basis_change': 'basis_change'}

FILTER_OUTPUT_DICT = {'an_yang': '_PRE', 'lee_refined': '_LEE', 'orientation_compensation': '_POC', 'basis_change': '_ELL'}

INPUT_OUTPUT_FORMATS_DICT = {'S2C3': 'change', 'S2C4': 'change', 'S2T3': 'change', 'S2T4': 'change', 'C2': 'unchanged',
                             'C3': 'unchanged', 'C4': 'unchanged', 'T2': 'unchanged', 'T3': 'unchanged',
                             'T4': 'unchanged', 'SPP': 'unchanged', 'IPP': 'unchanged'}
