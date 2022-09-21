import os
import json
from utils.DataUtil import DataUtil
from utils.MonitorUtil import MonitorUtil
import chardet

class FileOpUtil(object):
    def __init__(self):
        pass

    # 判断目录是否为空
    @staticmethod
    def is_dir_empty(dir_path):
        tmp = os.listdir(dir_path)
        if len(tmp) > 0:
            return False
        else:
            return True

    # 判断目录是否为空或者有文件存在
    @staticmethod
    def is_last_dir(dir_path):
        flag = False
        tmp = os.listdir(dir_path)
        if len(tmp) > 0:
            for i in tmp:
                file_path = os.path.join(dir_path, i)
                if os.path.isfile(file_path):
                    flag = True
        else:
            flag = True
        return flag

    # 递归找出当前目录下属于最后一级的目录
    @staticmethod
    def get_subdir(dir_path, result):
        sub_files = os.listdir(dir_path)
        if len(sub_files) > 0:
            for i in sub_files:
                sub_dir = os.path.join(dir_path, i)
                if os.path.isdir(sub_dir):
                    if FileOpUtil.is_last_dir(sub_dir):
                        result.append(sub_dir)
                    tmp = os.listdir(sub_dir)
                    if len(tmp) > 0:
                        FileOpUtil.get_subdir(sub_dir, result)

    # 递归找出当前目录下的所有子目录
    @staticmethod
    def get_all_subdir(dir_path, result):
        sub_files = os.listdir(dir_path)
        # print(sub_files)
        if len(sub_files) > 0:
            for i in sub_files:
                sub_dir = os.path.join(dir_path, i)
                if os.path.isdir(sub_dir):
                    result.append(sub_dir)
                    tmp = os.listdir(sub_dir)
                    if len(tmp) > 0:
                        FileOpUtil.get_subdir(sub_dir, result)

    # 递归找出当前目录下符合要求的文件
    @staticmethod
    def get_files(dir_path, result, patterns, dir_path_str):
        sub_files = os.listdir(dir_path)
        if len(sub_files) > 0:
            for i in sub_files:
                sub_file_path = os.path.join(dir_path, i)
                # print(sub_file_path)
                if os.path.isdir(sub_file_path):
                    tmp = os.listdir(sub_file_path)
                    if len(tmp) > 0:
                        FileOpUtil.get_files(sub_file_path, result, patterns, dir_path_str)
                else:
                    parent_dir = os.path.dirname(sub_file_path)
                    relative_path = parent_dir.replace(dir_path_str, "").replace("\\", "/")
                    # print(relative_path)
                    if relative_path not in patterns:
                        result.append(sub_file_path)

    # 获取指定目录下的所有文件
    @staticmethod
    # @MonitorUtil.func_time
    def get_files_dirs(dirs_path):
        """
        :param dirs_path: list
        :return: dict {fileName: fileAbsPath}
        """
        res = {}
        try:
            # for i in dirs_path: # 文件路径是['']的格式，空格内是提交文件目录
                # print('i:',i)
            tmp = os.listdir(dirs_path) # 只有一个文件目录-图片目录
            # print('tmp:',tmp)
            for j in tmp:
                file_path = dirs_path.replace("\\", "/") + "/" + j
                # print(file_path)
                if os.path.isfile(file_path):
                    res[j.split(".")[0]] = file_path
                    # print(res)
        except Exception as e:
            print(e)
        return res

        # 校验文件是否为JSON格式
    # 判断编码格式

    def detect_utf8(file_path):
        check_res = {}
        msg = None
        content = None
        state = True
        f3 = open(file=file_path, mode='rb')  # 以二进制模式读取文件
        data = f3.read()  # 获取文件内容
        # print(data)
        f3.close()  # 关闭文件
        result = chardet.detect(data)
        # print(result["encoding"])
        if result["encoding"] == "ascii":
            state = True
            check_res["state"] = state
            check_res["msg"] = msg
        else:
            state = False  # 报错
            msg = "文件编码格式错误"
            check_res["state"] = state
            check_res["msg"] = msg
        return check_res

    @staticmethod
    def is_file_json(file_path):
        """
        :param file_path: str
        :return:
        """
        check_res = {}
        msg = None
        content = None
        try:
            fp = open(file_path, encoding='utf-8')
            # print(fp)
            json_res = json.load(fp)
            # print(json_res)
            fp.close()
            state = True
            content = json_res
        except json.decoder.JSONDecodeError as e:
            state = False
            msg = "文件无法解析为JSON格式，具体原因：" + e.__str__()
        check_res["state"] = state
        check_res["msg"] = msg
        check_res["content"] = content
        return check_res

    @staticmethod
    def get_file_num(dirs, screen):
        num = 0
        for i in dirs:
            tmp = os.listdir(i)
            for j in tmp:
                file_path = i.replace("\\", "/") + "/" + j
                if os.path.isfile(file_path):
                    tmp1 = j.split(".")
                    if len(tmp1) == 2:
                        if tmp1[1] == screen:
                            num = num + 1
        return num

    @staticmethod
    def get_first_floor(dir_path):
        res = []
        if os.path.isdir(dir_path):
            tmp = os.listdir(dir_path)
            if len(tmp) > 0:
                for i in tmp:
                    path = dir_path.replace("\\", "/") + "/" + i
                    if os.path.isdir(path):
                        res.append(path)
        return res

    # 获取指定路径下面的所有可能的文件
    @staticmethod
    def get_possible_files_recursion(dir_path, screen, result, file_flag):
        """
        :param dir_path: str
        :param screen: list or None
        :param result: list
        :param file_flag: str filepath or filename
        :return:
        """
        tmp = os.listdir(dir_path)
        if len(tmp) > 0:
            for i in tmp:
                file_path = dir_path.replace("\\", "/") + "/" + i
                if os.path.isfile(file_path):
                    if screen is not None:
                        tmp = i.split(".")
                        suffix = ""
                        if len(tmp) == 2:
                            suffix = tmp[1]
                        elif len(tmp) > 2:
                            suffix = ".".join(tmp[1:])
                        if suffix == screen:
                            if file_flag == "filename":
                                result.append[i]
                            elif file_flag == "filepath":
                                result.append[file_path]
                    else:
                        if file_flag == "filename":
                            result.append[i]
                        elif file_flag == "filepath":
                            result.append[file_path]
                elif os.path.isdir(file_path):
                    FileOpUtil.get_possible_files_num(file_path, screen, result, file_flag)

    @staticmethod
    def get_possible_files(dirs_path, screen, result, file_flag):
        """
        :param dirs_path:
        :param screen:
        :param result: list
        :param file_flag:
        :return:
        """
        for i in dirs_path:
            tmp = os.listdir(i)
            for j in tmp:
                file_path = i.replace("\\", "/") + "/" + j
                if os.path.isfile(file_path):
                    if screen is not None:
                        tmp1 = i.split(".")
                        suffix = ""
                        if len(tmp1) == 2:
                            suffix = tmp1[1]
                        elif len(tmp1) > 2:
                            suffix = ".".join(tmp1[1:])
                        if suffix == screen:
                            if file_flag == "filename":
                                result.append[i]
                            elif file_flag == "filepath":
                                result.append[file_path]
                    else:
                        if file_flag == "filename":
                            result.append[i]
                        elif file_flag == "filepath":
                            result.append[file_path]

    @staticmethod
    def join_path(p_dir, sub_dirs):
        """
        :param p_dir: str
        :param sub_dirs: list
        :return:
        """
        res = []
        p_dir_format = p_dir.replace("\\", '/')
        if p_dir_format[-1] == "/":
            p_dir_format = p_dir_format[:-1]
        for i in sub_dirs:
            if i[0] == "/":
                tmp = i[1:]
            else:
                tmp = i
            sub_dir_path = p_dir_format + "/" + tmp
            res.append(sub_dir_path)
        return res

    @staticmethod
    def get_file_by_filename(files_kv, filename, replace_str):
        file_path = None
        if filename in files_kv:
            file_path = files_kv[filename]
        else:
            pattern_num = len(replace_str)
            label_num = len(filename)
            if label_num > pattern_num:
                label_prefix = DataUtil.str_replace(filename, replace_str)
                if label_prefix in files_kv:
                    file_path = files_kv[label_prefix]
        return file_path

    @staticmethod
    def write_result(file_path, content):
        try:
            with open(file_path, "w") as fp:
                fp.write(content)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def split_files(filenames, single_size):
        res = []
        files_num = len(filenames)
        if files_num > single_size:
            remainder = files_num % single_size
            if remainder != 0:
                new_file_num = int(files_num / single_size) + 1
            else:
                new_file_num = int(files_num / single_size)
            for i in range(1, new_file_num):
                start = (i - 1) * single_size
                end = i * single_size
                res.append({"start": start, "end": end})
            start = (new_file_num - 1) * single_size
            end = files_num
            res.append({"start": start, "end": end})
        else:
            start = 0
            end = files_num
            res.append({"start": start, "end": end})
        return res

    @staticmethod
    def join_paths(p_dir, sub_path):
        p_dir_list = []
        sub_path_list = []
        for i in p_dir.split("/"):
            if i != "":
                p_dir_list.append(i)
        for j in sub_path.split("/"):
            if j != "":
                sub_path_list.append(j)
        if p_dir[0] == "/":
            path = "/" + "/".join(p_dir_list + sub_path_list)
        else:
            path = "/".join(p_dir_list + sub_path_list)
        return path
