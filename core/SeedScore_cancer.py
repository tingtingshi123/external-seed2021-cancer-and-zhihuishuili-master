from core.Check_cancer import Check
from core.GetFilesInfo import GetFilesInfo
from utils.MonitorUtil import MonitorUtil
from utils.Fileoputil import FileOpUtil
from core.CheckPic import CheckPic
from score_fun.PAScore import PAScore
import json
from core.error_code import ErrorCode
import numpy as np
from score_fun.Top_1_Error import Top_1_Error
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
        effective_dirs_images=effective_dirs[0]+'/result' # 提交结果解压后的图片文件地址
        effective_dirs_label=effective_dirs[0]+'/result.csv'# 提交结果解压后的图片标签文件地址
        answer_dirs_image=self.answer_dirs[0]+'/result' # 答案的图片文件地址
        answer_dirs_label = self.answer_dirs[0] + '/result.csv'  # 答案的图片标签文件地址

        # 加载文件(图片文件)
        # print("#############获取提交文件名（文件数）、答案文件名（文件数）#############")
        submit_files = self.get_submit_files(effective_dirs_images)
        answer_files = self.get_answer_files(answer_dirs_image)
        submit_files = [i for i in submit_files if i != '']  # 去除mac本提交的非jpg或Png格式文件
        print("提交图片文件数：" + str(len(submit_files)))
        print("答案图片文件数：" + str(len(answer_files)))
        # 加载文件(标签文件)

        print("#############对提交的作品文件是否齐全进行判断#############")

        if len(submit_files) == len(answer_files):
            # print('提交的图片文件个数匹配')
            pass
        else:
            content = {"status": "failed", "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.LabelFileNotCompleteCode.value,
                       "errorMessage": ErrorCode.LabelFileNotComplete.value+"：提交作品数量："+str(len(submit_files))}
            FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
            if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                raise Exception("can not save result into target file")
            exit()

        print("#############获取有效目录下的所有文件，键值对形式#############")
        submit_file_kv = FileOpUtil.get_files_dirs(effective_dirs_images)
        # print(submit_file_kv)#{'2241': 'D:/python_tensorflow_mars/Competition_2021/evaluate_result/zip_file/result/result/2241.png'}

        # print("#############获取答案目录下的所有png文件，键值对形式#############")

        answer_file_kv = FileOpUtil.get_files_dirs(answer_dirs_image)
        # print(answer_file_kv)

        print("######################检查提交的图片内容(有效)##################################")
        real_submit_kv = {} # 真正命中的图片答案键值对{图片名称：图片名称地址}保存的文件是png格式的且文件名在答案中出现的文件
        count = 0
        names = list(answer_file_kv.keys())  # 答案中文件名列表
        names_det = list(submit_file_kv.keys())  # 提交的文件名称列表
        names_det = [i for i in names_det if i != '']
        # print(names_det)
        # if len(names_det) > 0: # 如果提交的文件不为空（图片不为空）(因为作品要求完整，所以已经满足完整条件，不需要在判断样本数量)
        for image_name in names_det:  # 对提交的每个文件名
            if image_name in names:  # 若文件名在答案文件名里
                abs_label_path = submit_file_kv[image_name]  # 有效的图片名对应的图片地址
                # print(abs_label_path)  # D:/python_tensorflow_mars/Competition_2021/evaluate_result/zip_file/result/result/2241.png
                # 检测每一个图像文件中的文件是否是png格式
                check_label = CheckPic(abs_label_path, self.compatible_file_suffix,list0=[0, 255])
                # print(check_label) #<core.CheckPic.CheckPic object at 0x0000020C382065E0>
                file_kv = check_label.fun()
                # print('检测结果：',file_kv)   # 测试时打开 检测结果： {'2241': 'D:/python_tensorflow_mars/Competition_2021/evaluate_result/zip_file/result/result/2241.png', 'state': True, 'msg': None}
                if file_kv["state"] is True:  # 图片是png格式
                    removed = file_kv.pop("state")
                    real_submit_kv[image_name] = file_kv[image_name]
                    count += 1
                else: # 不是png格式或像素不在【0,255】内

                    content = {"status": "failed", "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.LabelFileContentCode.value,
                               "errorMessage": file_kv["msg"]}
                    print(content)
                    FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                    if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                        raise Exception("can not save result into target file")
                    exit()
            # 若提交的文件名不在答案文件名里
            else:
                content = {"status": "failed","scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.FileIsMask.value,
                           "errorMessage": ErrorCode.FileIsMaskMsg.value}
                FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                    raise Exception("can not save result into target file")
                exit()

        # else:
        #     print('提交图片为空')
        #     pass

        # print('有效提交图片数量：', count)
        print("######################检查提交的标签文件(有效)##################################")
        real_submit_label = pd.DataFrame()
        label_count = 0
        # 判断文件是否存在
        if os.path.exists(effective_dirs_label):
            # 标签文件中的列名
            with open(effective_dirs_label, 'rb') as f:
                submit_label_file=f.read()
                # 判断文件编码方式
                file_encoding = chardet.detect(submit_label_file).get('encoding')
                # print('文件编码方式：',file_encoding)
                if file_encoding is None:
                    content = {"status": "failed", "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0},
                               "errorCode": ErrorCode.ImageNameNotExistsCode.value,
                               "errorMessage": "请检查提交的标签文件"}
                    FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                    if not FileOpUtil.write_result(self.score_res_path,
                                                   json.dumps(content, ensure_ascii=False)):
                        raise Exception("can not save result into target file")
                    exit()
                else:
                    if file_encoding=='UTF-8-SIG':
                        content = {"status": "failed", "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0},
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
                if len(answer_label_file) < len(submit_label_file):
                    content = {"status": "failed","scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0},
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
                        names_det = list(submit_label_file['image_name'])  # 提交中文件名列表
                        names = list(answer_label_file['image_name'])# 答案中文件名列表
                        if len([name for name in names_det if name in names])==len(names): # 提交的的文件与答案文件相同（个数可能多余答案个数）
                            real_submit_label=submit_label_file
                        else:
                            content = {"status": "failed","scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0},
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
                        content = {"status": "failed", "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.ColumnNameNotExistsCode.value,
                                   "errorMessage": ErrorCode.ColumnNameNotExists.value}
                        FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
                        if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                            raise Exception("can not save result into target file")
                        exit()
        else:# 标签文件不存在
            content = {"status": "failed","scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.LabelFileNotExistscode.value,
                       "errorMessage": ErrorCode.LabelFileNotExists.value}
            FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
            if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                raise Exception("can not save result into target file")
            exit()

        # 答案标签文件
        # answer_label={i:j for i,j in zip(answer_label_file["image_name"],answer_label_file["label"])}
        answer_label=answer_label_file
        print("#############获取PAScore评分#############")
        score = PAScore(answer_file_kv, real_submit_kv)

        score = score.fun()

        if np.isnan(score) == True:  # 提交空有效文件得分
            pa_score = 0
        else:
            pa_score = score

        print('\nPAScore得分:', pa_score)
        # print("#############获取Top_1_Error错误率#############")

        error = Top_1_Error(answer_label,real_submit_label)
        error = error.fun()

        if np.isnan(error) == True:  # 提交空有效文件得分
            error_score = 1
        else:
            error_score = error
        print('\nTop_1_Error得分:', error_score)
        score=0.7*pa_score+0.3*(1-error_score)
        print('\n综合得分:', score)
        content = {"status": "succeed","scoreObject":{"PAScore": pa_score,"Top_1_Error":error_score, "score": score}, "errorCode": 0, "errorMessage": ""}
        FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
        if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
            raise Exception("can not save result into target file")

