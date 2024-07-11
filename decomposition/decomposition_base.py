import os

from constants.decomposition_constants import DECOMPOSITION_TYPES, get_details


class DecompositionBase:
    def __init__(self, decomposition_type, output_dir: str, status):
        self.decomposition_type = decomposition_type
        self.decomposition_type_valid()
        self.output_dir = output_dir
        self.__status = status

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
        visible_file_suffix = []
        for suffix in output_path.visible_suffix:
            visible_file_suffix.append(decomposition_name + suffix)
        file['visible'] = visible_file_suffix
        print(file)
        return file

    def update_status(self, status):
        self.__status = status


if __name__ == '__main__':
    yamaguchi4 = DecompositionBase('Yamaguchi4_Y4O', './', 'finished')
    yamaguchi4.join_file_name()
