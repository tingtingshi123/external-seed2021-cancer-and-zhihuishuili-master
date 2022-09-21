from core.Check_cancer import Check
from core.GetFilesInfo import GetFilesInfo
from utils.MonitorUtil import MonitorUtil
from utils.Fileoputil import FileOpUtil
import json
from core.error_code import ErrorCode
import numpy as np
from score_fun.F1_Score import F1_score
import os
import pandas as pd
from core.CheckPic_label import CheckPic_label
import chardet

class SeedScore(object):
    def __init__(self, score_action_dir, score_res_path, label_file_name, answer_dirs, #tc_images_dirs,
                 coordinate_start,compatible_file_suffix, label_p_dir_name, appoint_dir_tree):
        self.score_action_dir = score_action_dir
        self.score_res_path = score_res_path
        self.label_file_name = label_file_name
        self.answer_dirs = answer_dirs
        # self.tc_images_dirs = tc_images_dirs
        self.coordinate_start = coordinate_start
        self.compatible_file_suffix = compatible_file_suffix
        self.label_p_dir_name = label_p_dir_name
        self.appoint_dir_tree = appoint_dir_tree

    # @MonitorUtil.func_time
    def get_answer_files(self,answer_dirs):
        res = []
        # for i in answer_dirs:
            # res = res + self.fetch_files(i)
        res = res + GetFilesInfo.focusight_get_file_name(answer_dirs)
        return res

    # @MonitorUtil.func_time
    def get_submit_files(self, submit_dirs):
        res = []
        # for i in submit_dirs:
        # for i in os.listdir(submit_dirs):
        #     print(i)
        res = res + GetFilesInfo.focusight_get_file_name(submit_dirs)
        return res



    @MonitorUtil.func_time
    def fun(self):
        # 检查基础环境、校验标注文件
        check = Check(self.score_action_dir, self.score_res_path, self.label_file_name, self.answer_dirs,
                      self.label_p_dir_name, self.appoint_dir_tree)

        check_res = check.fun()
        # print(check_res)

        effective_dirs = check_res["check_dir_format_res"]["effective_dirs"]
        # print('有效目录：', effective_dirs)

        effective_dirs_label=effective_dirs[0]+'/result.csv'# 提交结果解压后的图片标签文件地址
        answer_dirs_label = self.answer_dirs[0] + '/result.csv'  # 答案的图片标签文件地址

        print("######################检查提交的标签文件(有效)##################################")
        # 真正提交的有用的标签文件
        real_submit = pd.DataFrame()
        label_count = 0
        # 判断文件是否存在
        if os.path.exists(effective_dirs_label):
            # 标签文件中的列名
            with open(effective_dirs_label, 'rb') as f:
                submit_label_file = f.read()
                # 判断文件编码方式
                file_encoding = chardet.detect(submit_label_file).get('encoding')
                # print('文件编码方式：',file_encoding)
                if file_encoding is None:  # 空文件
                    content = {"status": "failed", "result": 0,
                               "errorCode": ErrorCode.ImageNameNotExistsCode.value,
                               "errorMessage": "请检查提交的标签文件"}
                    FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                    if not FileOpUtil.write_result(self.score_res_path,
                                                   json.dumps(content, ensure_ascii=False)):
                        raise Exception("can not save result into target file")
                    exit()
                else:
                    if file_encoding=='UTF-8-SIG':
                        content = {"status": "failed", "result": 0,
                                   "errorCode": ErrorCode.ImageNameNotExistsCode.value,
                                   "errorMessage": "读取文件超时，请提交正确的编码格式文件"}
                        FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                        if not FileOpUtil.write_result(self.score_res_path,
                                                       json.dumps(content, ensure_ascii=False)):
                            raise Exception("can not save result into target file")
                        exit()
                        pass
                    else:
                        submit_label_file = pd.read_csv(effective_dirs_label, engine='python',encoding=file_encoding)

                    answer_label_file = pd.read_csv(answer_dirs_label)
                    if len(answer_label_file)<len(submit_label_file):
                        content = {"status": "failed", "result": 0,
                                   "errorCode": ErrorCode.TimeOutCode.value,
                                   "errorMessage": "请提交指定数量的标签文件"}
                        FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                        if not FileOpUtil.write_result(self.score_res_path,
                                                       json.dumps(content, ensure_ascii=False)):
                            raise Exception("can not save result into target file")
                        exit()
                    else:
                        # 检测列名是否存在
                        check_columns=CheckPic_label(submit_label_file,answer_label_file).fun()
                        # print('检测标签内容：',check_columns)
                        if check_columns["state"] is True:# 列名正确
                            import operator
                            names_det = list(submit_label_file['image_name'])  # 提交中文件名列表
                            names = list(answer_label_file['image_name'])# 答案中文件名列表
                            # 判断集合是否包含相同的元素，相同结果为FALSE
                            if set(names_det).isdisjoint(set(names))==False:
                                real_submit=submit_label_file
                            else:
                                content = {"status": "failed", "result": 0,
                                           "errorCode": ErrorCode.ImageNameNotExistsCode.value,
                                           "errorMessage": "提交的图片标签数量与要求的标签数量不匹配"}
                                FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                                if not FileOpUtil.write_result(self.score_res_path,
                                                               json.dumps(content, ensure_ascii=False)):
                                    raise Exception("can not save result into target file")
                                exit()
                                pass
                        # print('有效提交图片标签数量：', label_count)
                        else:#列名不存在
                            content = {"status": "failed", "result": 0, "errorCode": ErrorCode.ColumnNameNotExistsCode.value,
                                       "errorMessage": check_columns["msg"]}
                            FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                            if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                                raise Exception("can not save result into target file")
                            exit()
        else:# 标签文件不存在
            content = {"status": "failed", "result": 0, "errorCode": ErrorCode.LabelFileNotExistscode.value,
                       "errorMessage": ErrorCode.LabelFileNotExists.value}
            FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
            if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                raise Exception("can not save result into target file")
            exit()
        # 读取答案标签文件
        answer=answer_label_file
        print("#############获取F1_score得分############")

        score = F1_score(real_submit,answer)
        f1_score = score.f1()

        if np.isnan(f1_score) == True:  # 提交空有效文件得分
            f1_score = 0
        else:
            f1_score = f1_score
        print('\nF1_score:', f1_score)
        content = {"status": "succeed", "result": f1_score, "errorCode": 0, "errorMessage": ""}
        FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
        if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
            raise Exception("can not save result into target file")

