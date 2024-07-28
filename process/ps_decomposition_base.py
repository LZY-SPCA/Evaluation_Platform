import os

from constants.decomposition_constant import DECOMPOSITION_TYPES, PROCESSING, FINISHED
from util.process_constant import get_decomposition_details


class DecompositionBase:
    def __init__(self, decomposition_type, output_dir: str):
        self.decomposition_type = decomposition_type
        self.decomposition_type_valid()
        self.output_dir = output_dir
        self.__status = PROCESSING

    def decomposition_type_valid(self):
        if self.decomposition_type not in DECOMPOSITION_TYPES:
            self.decomposition_type = None
            raise ValueError(f'Decomposition type must be one of {DECOMPOSITION_TYPES}')

    def join_file_name(self):
        decomposition_name = self.decomposition_type
        output_path = get_decomposition_details(decomposition_name)
        file = {}
        for channel, name in output_path.channel.items():
            channel_file = []
            for suffix in output_path.channel_suffix:
                channel_file.append(os.path.join(self.output_dir, decomposition_name + name + suffix))
            file[channel] = channel_file

        if output_path.visible is not None:
            visible_file_suffix = []
            for suffix in output_path.visible:
                visible_file_suffix.append(os.path.join(self.output_dir, decomposition_name + suffix))
            file['visible'] = visible_file_suffix

        if output_path.mask is not None:
            mask_file_suffix = []
            for suffix in output_path.mask:
                mask_file_suffix.append(os.path.join(self.output_dir, decomposition_name + suffix))
            file['mask'] = mask_file_suffix
        print(file)
        return file

    def update_status(self):
        if self.check_output_valid() is True:
            self.__status = FINISHED
        else:
            self.__status = PROCESSING

    def check_output_valid(self):
        file_dict = self.join_file_name()
        for f_list in file_dict.values():
            if type(f_list) is dict:
                for f_name in f_list:
                    if not os.path.exists(f_name):
                        f_list.remove(f_name)
            else:
                for f_name in f_list:
                    if not os.path.exists(f_name):
                        f_list.remove(f_name)
        return file_dict

    def get_status(self):
        return self.__status


if __name__ == '__main__':
    yamaguchi4 = DecompositionBase('Yamaguchi4_Y4O', './')
    yamaguchi4.join_file_name()
