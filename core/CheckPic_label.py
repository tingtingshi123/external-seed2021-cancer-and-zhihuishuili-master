from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None


class CheckPic_label(object):
    def __init__(self, submit_label_file,answer_label_file):
        """
            :param label_path: string 文件路径
            :param tc_images_list: list
            :param correct_list: list
        """
        self.submit_label_file = submit_label_file
        self.answer_label_file = answer_label_file


    # 校验文件列名是否存在
    def is_file_columns(self, submit_label_file):
        check_res = {}
        msg = None
        state = False
        try:
            # 标签文件中的列名
            submit_file_columns=submit_label_file.columns.tolist()
            # print('提交的列名：',submit_file_columns)
            if 'image_name' in submit_label_file and 'label' in submit_label_file \
                    and len(submit_file_columns)==2:
                state = True
                msg = None
            else:
                msg = "标签文件中的列名不符合要求"
                state = False
        except Exception as e:
            print(e)

        check_res["state"] = state
        check_res["msg"] = msg
        return check_res

    # 检查标签样本个数
    def check_label_nums(self):
        check_res = {}
        msg = None
        state = False
        try:
            # 答案类别
            answer_type = list(set(self.answer_label_file.label.values))
            # print('答案类别：', answer_type)
            # 提交类别
            submit_type = list(set(self.submit_label_file.label.values))
            # print('提交类别：', submit_type)
            if len(set(submit_type))==len(self.answer_label_file):
            # if len([np.isnan(i) for i in submit_type])==len(answer_type):
                # print('提交结果全为空!')
                msg='提交结果全为空!'
                state = False
            else:
                state = True
                msg = None
        except Exception as e:
            print(e)
        check_res["state"] = state
        check_res["msg"] = msg
        return check_res




    def check_jpg_structure(self, submit_label_file):

        is_correct = self.is_file_columns(submit_label_file)
        label_nums=self.check_label_nums()
        # print('检测结构：',is_correct)
        if is_correct["state"] is False: # 判断列名是否正确
            return is_correct
        else:
            # print(is_correct)
            # print(label_nums)
            if label_nums["state"] is False:
                return label_nums
            else:
                return is_correct



    # fun函数
    def fun(self):
        file_kv = self.check_jpg_structure(self.submit_label_file)
        # print('检测结果：',file_kv)
        if file_kv["state"] is False:
            return file_kv
        else:
            return file_kv
