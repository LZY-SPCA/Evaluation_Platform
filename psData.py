import numpy as np


def T_matrix_valid(T_matrix: np.array) -> bool:
    shape = T_matrix.shape
    if len(shape) == 4 and shape[2] == 3 and shape[3] == 3:
        return True
    return False


def S_matrix_valid(S_matrix: np.array) -> bool:
    shape = S_matrix.shape
    if len(shape) == 4 and shape[2] == 2 and shape[3] == 2:
        return True
    return False


class PolSARData:
    def __init__(self, proj_name, height, width):
        self.proj_name = proj_name
        self.height = height
        self.width = width
        self.S_matrix = None
        self.T_matrix = None
        self.S_matrix_exist = False
        self.T_matrix_exist = False

    def set_S_matrix(self, S_matrix: np.array):
        if S_matrix is not None and S_matrix_valid(S_matrix):
            self.S_matrix = S_matrix
            self.S_matrix_exist = True

    def get_S_matrix(self) -> np.array:
        return self.S_matrix

    def set_T_matrix(self, T_matrix: np.array):
        if T_matrix is not None and T_matrix_valid(T_matrix):
            self.T_matrix = T_matrix
            self.T_matrix_exist = True

    def get_T_matrix(self) -> np.array:
        return self.T_matrix
