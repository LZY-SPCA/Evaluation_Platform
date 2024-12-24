import os

from constants.decomposition_constant import DECOMPOSITION_TYPES, PROCESSING, FINISHED
from util.constant_process import get_decomposition_details


class DecompositionBase:
    def __init__(self, decomposition_type, output_dir: str):
        self.decomposition_type = decomposition_type
        self.decomposition_type_valid()
        self.output_dir = output_dir
        self.output_files = self.join_file_name()
        self.__status = PROCESSING

    def decomposition_type_valid(self):
        if self.decomposition_type not in DECOMPOSITION_TYPES:
            self.decomposition_type = None
            raise ValueError(f'Decomposition type must be one of {DECOMPOSITION_TYPES}')

    def join_file_name(self, **kwargs):
        """
        基于不同分解类型拼接输出文件的名称
        :return:
        """
        decomposition_name = self.decomposition_type
        output_path = get_decomposition_details(decomposition_name)
        file = {}
        for channel, name in output_path.channel.items():
            channel_file = []
            for suffix in output_path.channel_suffix:
                channel_file.append(os.path.join(self.output_dir, name + suffix))
            file[channel] = channel_file

        if output_path.visible is not None:
            visible_file_suffix = []
            for suffix in output_path.visible:
                visible_file_suffix.append(os.path.join(self.output_dir, suffix))
            file['visible'] = visible_file_suffix

        if output_path.mask is not None:
            mask_file_suffix = []
            for suffix in output_path.mask:
                mask_file_suffix.append(os.path.join(self.output_dir, suffix))
            file['mask'] = mask_file_suffix
        print(file)
        return file

    def check_output_valid(self):
        """
        检查输出文件是否有效（是否生成输出文件）
        :return:
        """
        file_dict = self.output_files
        for f_list in file_dict.values():
            if type(f_list) is dict:
                for f_name in f_list:
                    if not os.path.exists(f_name):
                        f_list.remove(f_name)
            else:
                for f_name in f_list[:]:
                    if not os.path.exists(f_name):
                        f_list.remove(f_name)
        for key in list(file_dict.keys()):
            if len(file_dict[key]) == 0:
                del file_dict[key]
        return file_dict

    def get_status(self):
        return self.__status


if __name__ == '__main__':
    yamaguchi4 = DecompositionBase('Yamaguchi4_Y4O', './')
    yamaguchi4.join_file_name()
    h_a_alpha = DecompositionBase('H_A_ALPHA', './')
    h_a_alpha.join_file_name()
    krogager = DecompositionBase('Krogager', './')
    krogager.join_file_name()
    krogager.check_output_valid()
