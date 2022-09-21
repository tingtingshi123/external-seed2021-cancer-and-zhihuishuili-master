import os
from utils.MyUtils import MyUtils
from PIL import Image
import cv2
import numpy as np
Image.MAX_IMAGE_PIXELS = None


class CheckPic(object):
    def __init__(self, label_path, compatible_file_suffix, list0):
        """
            :param label_path: string 文件路径
            :param tc_images_list: list
            :param correct_list: list
        """
        self.label_path = label_path
        self.compatible_file_suffix = compatible_file_suffix
        self.list0 = list0
        # self.size0 = size0 # 不判断图片尺寸

    # 校验文件是否为png格式
    def is_file_jpg(self, label_path):
        check_res = {}
        msg = None
        state = False
        try:
            if label_path.endswith('.png'):
                state = True
                msg = None
                image_name = os.path.split(label_path)[1].split('.')[0]
                check_res[os.path.split(label_path)[1].split('.')[0]] = label_path  # 文件名os.path.split(label_path)[1]
            else:
                msg = "文件无法解析为png格式"
                state = False
        except Exception as e:
            print(e)

        check_res["state"] = state
        check_res["msg"] = msg
        return check_res

    #

    # 检查文件件是否只有0,255

    def img_binary(self, label_path):  # 图像判断（是否只有0和255）
        '''

        :param label_path: 文件路径
        :param list0: 搜索列表
        :return:
        '''
        check_res = {}
        state = False
        msg=None
        try:
            image_info = Image.open(label_path)
            img_arr = np.array(image_info)
            list1 = np.unique(img_arr)
            # print('图像中像素值:',list1)
            no_exist = [False for a in list1 if a not in self.list0]
            if no_exist:
                state = False
                msg = "文件不是只有0和255"
            else:
                image_name = os.path.split(label_path)[1].split('.')[0]
                check_res[os.path.split(label_path)[1].split('.')[0]] = label_path
                state = True
        except Exception as e:
            print(e)
        check_res["state"] = state
        check_res['msg'] = msg
        return check_res

    # 检查文件结构
    def check_jpg_structure(self, label_path):
        check_res = {}
        state = True
        msg = None
        is_jpg = self.is_file_jpg(label_path)
        is_bi = self.img_binary(label_path)
        # print(is_bi)
        if is_jpg["state"] is False:
            return is_jpg
        else:
            if is_bi["state"] is False:
                return is_bi
            else:
                return is_bi



    # fun函数
    def fun(self):
        file_kv = self.check_jpg_structure(self.label_path)
        # print('file_kv:',file_kv)
        if file_kv["state"] is False:
            return file_kv
        else:
            return file_kv
# 检查文件大小是否是（2048,2048）
    #
    # def file_size(self, label_path):  # 图像尺寸判断  label_path为键值对
    #     '''
    #     :param label_path: 文件路径
    #     :param size0: 指定尺寸
    #     :return:
    #     '''
    #     check_res = {}
    #     state = False
    #     msg = None
    #     try:
    #         image_info = Image.open(label_path)
    #         size = image_info.size
    #         if size == self.size0:
    #             state = True  # os.path.splitext(file)[0] 获得文件名
    #             image_name = os.path.split(label_path)[1].split('.')[0]
    #             check_res[os.path.split(label_path)[1].split('.')[0]] = label_path
    #         else:
    #             state = True
    #             msg = "文件尺寸不是（2048,2048）"
    #             pass
    #     except Exception as e:
    #         print(e)
    #         msg = "文件尺寸不是（2048,2048）"
    #     check_res["state"] = state
    #
    #     check_res["msg"] = msg
    #     return check_res