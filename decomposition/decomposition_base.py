import os

from constants.decomposition_constants import DECOMPOSITION_TYPES, get_details, PROCESSING, FINISHED


class DecompositionBase:
    def __init__(self, decomposition_type, output_dir: str):
        self.decomposition_type = decomposition_type
        self.decomposition_type_valid()
        self.output_dir = output_dir
        self.__status = PROCESSING

    def decomposition_type_valid(self):
        if self.decomposition_type not in DECOMPOSITION_TYPES:
            self.decomposition_type = None
            raise ValueError('Decomposition type must be one of {}'.format(DECOMPOSITION_TYPES))

    def join_file_name(self):
        decomposition_name = self.decomposition_type
        file_path = os.path.join(self.output_dir, decomposition_name)
        output_path = get_details(decomposition_name)
        file = {}
        for channel, name in output_path.channel.items():
            channel_file = []
            for suffix in output_path.channel_suffix:
                channel_file.append(decomposition_name + name + suffix)
            file[channel] = channel_file

        if output_path.visible_suffix is not None:
            visible_file_suffix = []
            for suffix in output_path.visible_suffix:
                visible_file_suffix.append(decomposition_name + suffix)
            file['visible'] = visible_file_suffix

        if output_path.mask_suffix is not None:
            mask_file_suffix = []
            for suffix in output_path.mask_suffix:
                mask_file_suffix.append(decomposition_name + suffix)
            file['mask'] = mask_file_suffix
        print(file)
        return file

    def update_status(self, status):
        if status is not None:
            self.__status = status
        else:
            if self.check_output_valid() is True:
                self.__status = FINISHED
            else:
                self.__status = PROCESSING

    def check_output_valid(self):
        file_list = self.join_file_name()
        for f_list in file_list:
            if type(f_list) is dict:
                for f_name in f_list.values():
                    if not os.path.exists(self.output_dir + f_name):
                        return False
            else:
                for f_name in f_list:
                    if not os.path.exists(self.output_dir + f_name):
                        return False

    def get_status(self):
        return self.__status


if __name__ == '__main__':
    yamaguchi4 = DecompositionBase('Yamaguchi4_Y4O', './')
    yamaguchi4.join_file_name()
