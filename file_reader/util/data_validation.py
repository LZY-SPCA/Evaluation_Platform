import numpy as np


def data_consist_valid(dataset):
    shape = 0
    for matrix in dataset:
        if shape == 0:
            shape = np.shape(matrix)
        else:
            if shape != np.shape(matrix):
                raise Exception('channels not same size')
