from model.pol_sar_data import PolSARData
from ps_work_steps import WorkSteps
from constants.ps_constant import *


def check_process_procedure(work_steps: WorkSteps):
    data: PolSARData = work_steps.input_data
    rerun_list = []
    if not data.is_decomposition_empty():
        rerun_list.append(DECOMPOSITION_RERUN)
    if not data.is_detection_empty():
        rerun_list.append(DETECTION_RERUN)
    if not data.is_recognition_empty():
        rerun_list.append(RECOGNITION_RERUN)
    return rerun_list


def check_decomposition_procedure(work_steps: WorkSteps):
    data: PolSARData = work_steps.input_data
    rerun_list = []
    if not data.is_detection_empty():
        rerun_list.append(DETECTION_RERUN)
    if not data.is_recognition_empty():
        rerun_list.append(RECOGNITION_RERUN)
    return rerun_list


def check_detection_procedure(work_steps: WorkSteps):
    data: PolSARData = work_steps.input_data
    rerun_list = []
    if not data.is_recognition_empty():
        rerun_list.append(RECOGNITION_RERUN)
    return rerun_list
