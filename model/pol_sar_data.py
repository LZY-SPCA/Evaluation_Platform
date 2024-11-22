"""
    A class for storing polarization data
"""
import numpy as np
from constants.polarization_constant import FULL_POLARIZATION, DUAL_POLARIZATION


class PolSARData:
    def __init__(self, proj_name, height, width, polar_type, dual_type=None):
        """
        Initialise the polarization data
        :param proj_name: project name
        :param height: height of the polarization data
        :param width: width of the polarization data
        :param polar_type: type of polarization constant e.g. 'full'
        :param dual_type: type of dual_polarization constant e.g. 'PP1'
        """
        self.proj_name = proj_name
        self.height = height
        self.width = width
        self.polar_type = polar_type
        self.dual_type = dual_type
        self.__S_matrix = None
        self.__T_matrix = None
        self.__C_matrix = None
        self.__process = []
        self.__decomposition = []
        self.__detection = []
        self.__recognition = []
        self.S_matrix_exist = False
        self.T_matrix_exist = False
        self.C_matrix_exist = False

    def set_S_matrix(self, S_matrix: np.array):
        if S_matrix is not None and self.S_matrix_valid(S_matrix):
            self.__S_matrix = S_matrix
            self.S_matrix_exist = True

    def get_S_matrix(self) -> np.array:
        return self.__S_matrix

    def set_C_matrix(self, C_matrix: np.array) -> np.array:
        if C_matrix is not None and self.C_matrix_valid(C_matrix):
            if self.is_T_matrix_available():
                print("Already have T_matrix, unable to set C_matrix")
            else:
                self.__C_matrix = C_matrix
                self.C_matrix_exist = True

    def get_C_matrix(self) -> np.array:
        return self.__C_matrix

    def set_T_matrix(self, T_matrix: np.array):
        if T_matrix is not None and self.T_matrix_valid(T_matrix):
            if self.is_C_matrix_available():
                print("Already have C_matrix, unable to set T_matrix")
            else:
                self.__T_matrix = T_matrix
                self.T_matrix_exist = True

    def get_T_matrix(self) -> np.array:
        return self.__T_matrix

    def T_matrix_valid(self, T_matrix: np.array) -> bool:
        shape = T_matrix.shape
        if len(shape) == 4 and shape[0] == self.height and shape[1] == self.width:
            if self.polar_type == FULL_POLARIZATION and shape[2] == 3 and shape[3] == 3:
                return True
            elif self.polar_type == DUAL_POLARIZATION and shape[2] == 2 and shape[3] == 2:
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

    def C_matrix_valid(self, C_matrix: np.array) -> bool:
        shape = C_matrix.shape
        if len(shape) == 4 and shape[0] == self.height and shape[1] == self.width:
            if self.polar_type == FULL_POLARIZATION and shape[2] == 3 and shape[3] == 3:
                return True
            elif self.polar_type == DUAL_POLARIZATION and shape[2] == 2 and shape[3] == 2:
                return True
        return False

    def is_S_matrix_available(self):
        return self.S_matrix_exist

    def is_T_matrix_available(self):
        return self.T_matrix_exist

    def is_C_matrix_available(self):
        return self.C_matrix_exist

    def get_polar_type(self):
        return self.polar_type

    def get_dual_type(self):
        return self.dual_type

    def add_process(self, process_type):
        if process_type in self.__process:
            return False
        else:
            self.__process.append(process_type)
            return True

    def find_process(self, process_type):
        if process_type in self.__process:
            return True
        else:
            return False

    def is_process_empty(self):
        return len(self.__process) == 0

    def add_decomposition(self, decomposition_type):
        if decomposition_type in self.__decomposition:
            return False
        else:
            self.__decomposition.append(decomposition_type)
            return True

    def find_decomposition(self, decomposition_type):
        if decomposition_type in self.__decomposition:
            return True
        else:
            return False

    def is_decomposition_empty(self):
        return len(self.__decomposition) == 0

    def add_detection(self, detection_type):
        if detection_type in self.__detection:
            return False
        else:
            self.__detection.append(detection_type)
            return True

    def find_detection(self, detection_type):
        if detection_type in self.__detection:
            return True
        else:
            return False

    def is_detection_empty(self):
        return len(self.__detection) == 0

    def add_recognition(self, recognition_type):
        if recognition_type in self.__recognition:
            return False
        else:
            self.__recognition.append(recognition_type)
            return True

    def find_recognition(self, recognition_type):
        if recognition_type in self.__recognition:
            return True
        else:
            return False

    def is_recognition_empty(self):
        return len(self.__recognition) == 0
