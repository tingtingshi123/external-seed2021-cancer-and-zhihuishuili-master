import abc


class ClassifyByFileName(metaclass=abc.ABCMeta):
    # @abc.abstractmethod
    # def get_test_set_files(self):
    #     pass
    #
    # @abc.abstractmethod
    # def get_answer_files(self):
    #     pass
    #
    # @abc.abstractmethod
    # def get_submit_files(self):
    #     pass

    # @abc.abstractmethod
    # def get_ok_files(self, answer_files, tc_images_files):
    #     pass

    # @abc.abstractmethod
    # def get_potential_error_files(self, submit_files, test_set_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_correct_files(self, submit_files, test_set_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_hit_files(self, potential_correct_files, answer_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_escape_files(self, potential_correct_files, answer_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_overkill_files(self, potential_correct_files, answer_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_replaced_suffix_file(self, potential_error):
    #     pass
    #
    # @abc.abstractmethod
    # def add_suffix(self, compatible_str):
    #     pass
    #
    # # @abc.abstractmethod
    # # def classify_potential_error_file(self, potential_error, tc_files, answer_files):
    # #     pass
    #
    # @abc.abstractmethod
    # def fun(self):
    #     pass
    # @abc.abstractmethod
    # def get_potential_error_files(self, submit_files, test_set_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_correct_files(self, submit_files, test_set_files):
    #     pass

    @abc.abstractmethod
    def get_potential_hit_files(self, potential_correct_files, answer_files):
        pass

    # @abc.abstractmethod
    # def get_potential_escape_files(self, potential_correct_files, answer_files):
    #     pass
    #
    # @abc.abstractmethod
    # def get_potential_overkill_files(self, potential_correct_files, answer_files):
    #     pass

    @abc.abstractmethod
    def fun(self):
        pass
