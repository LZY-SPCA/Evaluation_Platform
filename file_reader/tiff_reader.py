from osgeo import gdal
import numpy as np
from pol_sar_data import PolSARData
from constants.constant import (FULL_POLARIZATION, DUAL_POLARIZATION, FULL_POLARIZATION_CHANNELS,
                                DUAL_POLARIZATION_CHANNELS, DUAL_POLARIZATION_TYPES)


gdal.UseExceptions()

C_path = '.\dat_tiff\C'
S_path = '.\data_tiff\S'
full_polarisation_mode = ['HH', 'HV', 'VH', 'VV']
dual_polarisation_mode = ['HH', 'VV']
datasets = []


def pre_process():
    dataset = gdal.Open(f'{C_path}/1144_010_C_HH_L1A.tiff', gdal.GA_ReadOnly)
    data = dataset.GetRasterBand(1).ReadAsArray()
    return data.shape


def read_full_as_SAR() -> PolSARData:
    shape = pre_process()
    for polar in FULL_POLARIZATION_CHANNELS:
        dataset = gdal.Open(f'{C_path}/1144_010_C_{polar}_L1A.tiff', gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1], datasets[2], datasets[3]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 2, 2)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1], FULL_POLARIZATION)
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


def read_dual_as_SAR(dual_type: int) -> PolSARData:
    shape = pre_process()
    for polar in DUAL_POLARIZATION_CHANNELS[dual_type]:
        dataset = gdal.Open(f'{C_path}/1144_010_C_{polar}_L1A.tiff', gdal.GA_ReadOnly)
        data = dataset.GetRasterBand(1).ReadAsArray()
        datasets.append(data)
    SAR_matrix = np.dstack((datasets[0], datasets[1]))
    SAR_matrix = SAR_matrix.transpose(1, 2, 0).reshape(shape[0], shape[1], 1, 2)
    sar_data = PolSARData('1144_010_C_HH_L1A', shape[0], shape[1],
                          DUAL_POLARIZATION, DUAL_POLARIZATION_TYPES[dual_type])
    sar_data.set_S_matrix(SAR_matrix)
    print(sar_data.is_S_matrix_available())
    return sar_data


if __name__ == '__main__':
    read_dual_as_SAR()
