import os
import json
from PIL import Image


class MyUtils(object):
    def __init__(self):
        pass

    # # 获取数据类型
    # @staticmethod
    # def get_data_type(class_info):
    #     return str(type(class_info)).replace("<class '", "").replace("'>", "")

    # # 判断目录是否为空
    # @staticmethod
    # def is_dir_empty(dir_path):
    #     tmp = os.listdir(dir_path)
    #     if len(tmp) > 0:
    #         return False
    #     else:
    #         return True

    # # 判断目录是否为空或者有文件存在
    # @staticmethod
    # def is_last_dir(dir_path):
    #     flag = False
    #     tmp = os.listdir(dir_path)
    #     if len(tmp) > 0:
    #         for i in tmp:
    #             file_path = os.path.join(dir_path, i)
    #             if os.path.isfile(file_path):
    #                 flag = True
    #     else:
    #         flag = True
    #     return flag

    # # 递归找出当前目录下属于最后一级的目录
    # @staticmethod
    # def get_subdir(dir_path, result):
    #     sub_files = os.listdir(dir_path)
    #     # print(sub_files)
    #     if len(sub_files) > 0:
    #         for i in sub_files:
    #             sub_dir = os.path.join(dir_path, i)
    #             if os.path.isdir(sub_dir):
    #                 if MyUtils.is_last_dir(sub_dir):
    #                     result.append(sub_dir)
    #                 tmp = os.listdir(sub_dir)
    #                 # lower_dir = sub_dir.replace(dir_path_str, "").replace("\\", "/").lower()
    #                 # tmp_dict = {"source_dir": sub_dir, "lower_dir": lower_dir}
    #                 # result.append(tmp_dict)
    #                 if len(tmp) > 0:
    #                     MyUtils.get_subdir(sub_dir, result)

    # # 递归找出当前目录下的所有子目录
    # @staticmethod
    # def get_all_subdir(dir_path, result):
    #     sub_files = os.listdir(dir_path)
    #     # print(sub_files)
    #     if len(sub_files) > 0:
    #         for i in sub_files:
    #             sub_dir = os.path.join(dir_path, i)
    #             if os.path.isdir(sub_dir):
    #                 result.append(sub_dir)
    #                 tmp = os.listdir(sub_dir)
    #                 if len(tmp) > 0:
    #                     MyUtils.get_subdir(sub_dir, result)

    # # 递归找出当前目录下符合要求的文件
    # @staticmethod
    # def get_files(dir_path, result, patterns, dir_path_str):
    #     sub_files = os.listdir(dir_path)
    #     if len(sub_files) > 0:
    #         for i in sub_files:
    #             sub_file_path = os.path.join(dir_path, i)
    #             # print(sub_file_path)
    #             if os.path.isdir(sub_file_path):
    #                 tmp = os.listdir(sub_file_path)
    #                 if len(tmp) > 0:
    #                     MyUtils.get_files(sub_file_path, result, patterns, dir_path_str)
    #             else:
    #                 parent_dir = os.path.dirname(sub_file_path)
    #                 relative_path = parent_dir.replace(dir_path_str, "").replace("\\", "/")
    #                 # print(relative_path)
    #                 if relative_path not in patterns:
    #                     result.append(sub_file_path)
    #
    # # 获取指定目录下的所有文件
    # @staticmethod
    # def get_files_dirs(dirs_path):
    #     """
    #     :param dirs_path: list
    #     :return: dict {fileName: fileAbsPath}
    #     """
    #     res = {}
    #     try:
    #         for i in dirs_path:
    #             tmp = os.listdir(i)
    #             for j in tmp:
    #                 file_path = i.replace("\\", "/") + "/" + j
    #                 if os.path.isfile(file_path):
    #                     res[j.split(".")[0]] = file_path
    #     except Exception as e:
    #         print(e)
    #     return res

    # @staticmethod
    # def str_replace(source_str, replace_str):
    #     replace_str_num = len(replace_str)
    #     i_suffix = source_str[-replace_str_num:]
    #     if i_suffix == replace_str:
    #         i_prefix = source_str[: -replace_str_num]
    #         return i_prefix
    #     else:
    #         return None

    # # 校验文件是否为JSON格式
    # @staticmethod
    # def is_file_json(file_path):
    #     """
    #     :param file_path: str
    #     :return:
    #     """
    #     check_res = {}
    #     msg = None
    #     content = None
    #     try:
    #         fp = open(file_path, encoding='utf-8')
    #         json_res = json.load(fp)
    #         fp.close()
    #         state = True
    #         content = json_res
    #     except json.decoder.JSONDecodeError as e:
    #         state = False
    #         msg = "文件无法解析为JSON格式，具体原因：" + e.__str__()
    #     check_res["state"] = state
    #     check_res["msg"] = msg
    #     check_res["content"] = content
    #     return check_res

    # @staticmethod
    # def get_file_num(dirs, screen):
    #     num = 0
    #     for i in dirs:
    #         tmp = os.listdir(i)
    #         for j in tmp:
    #             file_path = i.replace("\\", "/") + "/" + j
    #             if os.path.isfile(file_path):
    #                 tmp1 = j.split(".")
    #                 if len(tmp1) == 2:
    #                     if tmp1[1] == screen:
    #                         num = num + 1
    #     return num
    #
    # @staticmethod
    # def get_first_floor(dir_path):
    #     res = []
    #     if os.path.isdir(dir_path):
    #         tmp = os.listdir(dir_path)
    #         if len(tmp) > 0:
    #             for i in tmp:
    #                 path = dir_path.replace("\\", "/") + "/" + i
    #                 if os.path.isdir(path):
    #                     res.append(path)
    #     return res
    #
    # # 获取制定路径下面的所有可能的文件
    # @staticmethod
    # def get_possible_files_recursion(dir_path, screen, result, file_flag):
    #     """
    #     :param dir_path: str
    #     :param screen: list or None
    #     :param result: list
    #     :param file_flag: str filepath or filename
    #     :return:
    #     """
    #     tmp = os.listdir(dir_path)
    #     if len(tmp) > 0:
    #         for i in tmp:
    #             file_path = dir_path.replace("\\", "/") + "/" + i
    #             if os.path.isfile(file_path):
    #                 if screen is not None:
    #                     tmp = i.split(".")
    #                     suffix = ""
    #                     if len(tmp) == 2:
    #                         suffix = tmp[1]
    #                     elif len(tmp) > 2:
    #                         suffix = ".".join(tmp[1:])
    #                     if suffix == screen:
    #                         if file_flag == "filename":
    #                             result.append[i]
    #                         elif file_flag == "filepath":
    #                             result.append[file_path]
    #                 else:
    #                     if file_flag == "filename":
    #                         result.append[i]
    #                     elif file_flag == "filepath":
    #                         result.append[file_path]
    #             elif os.path.isdir(file_path):
    #                 MyUtils.get_possible_files_num(file_path, screen, result, file_flag)
    #
    # @staticmethod
    # def get_possible_files(dirs_path, screen, result, file_flag):
    #     for i in dirs_path:
    #         tmp = os.listdir(i)
    #         for j in tmp:
    #             file_path = i.replace("\\", "/") + "/" + j
    #             if os.path.isfile(file_path):
    #                 if screen is not None:
    #                     tmp1 = i.split(".")
    #                     suffix = ""
    #                     if len(tmp1) == 2:
    #                         suffix = tmp1[1]
    #                     elif len(tmp1) > 2:
    #                         suffix = ".".join(tmp1[1:])
    #                     if suffix == screen:
    #                         if file_flag == "filename":
    #                             result.append[i]
    #                         elif file_flag == "filepath":
    #                             result.append[file_path]
    #                 else:
    #                     if file_flag == "filename":
    #                         result.append[i]
    #                     elif file_flag == "filepath":
    #                         result.append[file_path]
    #
    # @staticmethod
    # def join_path(p_dir, sub_dirs):
    #     """
    #     :param p_dir: str
    #     :param sub_dirs: list
    #     :return:
    #     """
    #     res = []
    #     p_dir_format = p_dir.replace("\\", '/')
    #     if p_dir_format[-1] == "/":
    #         p_dir_format = p_dir_format[:-1]
    #     for i in sub_dirs:
    #         if i[0] == "/":
    #             tmp = i[1:]
    #         else:
    #             tmp = i
    #         sub_dir_path = p_dir_format + "/" + tmp
    #         res.append(sub_dir_path)
    #     return res
    #
    # @staticmethod
    # def get_file_by_filename(files_kv, filename, replace_str):
    #     file_path = None
    #     if filename in files_kv:
    #         file_path = files_kv[filename]
    #     else:
    #         pattern_num = len(replace_str)
    #         label_num = len(filename)
    #         if label_num > pattern_num:
    #             label_prefix = MyUtils.str_replace(filename, replace_str)
    #             if label_prefix in files_kv:
    #                 file_path = files_kv[label_prefix]
    #     return file_path

    # 获取像素坐标范围
    @staticmethod
    def get_image_hw(filepath):
        image_info = Image.open(filepath)
        size = image_info.size
        # print(size)
        width = size[0]
        height = size[1]
        return {"height": height, "width": width}

    # @staticmethod
    # def write_result(file_path, content):
    #     try:
    #         with open(file_path, "w") as fp:
    #             fp.write(content)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False

# tc_file_kv = {"aaaaa": "/aaa/ccc"}
# label_file_k = "aaaaabmp"
# pattern = "bmp"
# print(MyUtils.get_file_by_filename(tc_file_kv, label_file_k, pattern))