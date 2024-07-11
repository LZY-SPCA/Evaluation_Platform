import numpy as np
from constants.polarization_constant import FULL_POLARIZATION, DUAL_POLARIZATION


class PolSARData:
    def __init__(self, proj_name, height, width, polar_type, dual_type=None):
        self.proj_name = proj_name
        self.height = height
        self.width = width
        self.polar_type = polar_type
        self.dual_type = dual_type
        self.__S_matrix = None
        self.__T_matrix = None
        self.S_matrix_exist = False
        self.T_matrix_exist = False

    def set_S_matrix(self, S_matrix: np.array):
        if S_matrix is not None and self.S_matrix_valid(S_matrix):
            self.__S_matrix = S_matrix
            self.S_matrix_exist = True

    def get_S_matrix(self) -> np.array:
        return self.__S_matrix

    def set_T_matrix(self, T_matrix: np.array):
        if T_matrix is not None and self.T_matrix_valid(T_matrix):
            self.__T_matrix = T_matrix
            self.T_matrix_exist = True

    def get_T_matrix(self) -> np.array:
        return self.__T_matrix

    def T_matrix_valid(self, T_matrix: np.array) -> bool:
        shape = T_matrix.shape
        if (len(shape) == 4 and shape[0] == self.height and shape[1] == self.width
                and shape[2] == 3 and shape[3] == 3):
            return True
        return False

    def S_matrix_valid(self, S_matrix: np.array) -> bool:
        shape = S_matrix.shape
        if len(shape) == 4 and shape[0] == self.height and shape[1] == self.width:
            if self.polar_type == FULL_POLARIZATION and shape[2] == 2 and shape[3] == 2:
                return True
            elif self.polar_type == DUAL_POLARIZATION and shape[2] == 1 and shape[3] == 2:
                return True
        return False

    def is_S_matrix_available(self):
        return self.S_matrix_exist

    def is_T_matrix_available(self):
        return self.T_matrix_exist

    def get_polar_type(self):
        return self.polar_type

    def get_dual_type(self):
        return self.dual_type
