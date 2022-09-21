import os
import json
import shutil
import time
from core.error_code import ErrorCode
from core.CheckSubmitDirFormat import CheckSubmitDirFormat
import core.myzipfile as zipfile
from utils.Fileoputil import FileOpUtil


class Check(object):
    def __init__(self, score_action_dir, score_res_path, label_file_name, answer_dirs, label_p_dir_name,
                 appoint_dir_tree):
        self.score_action_dir = score_action_dir
        self.score_res_path = score_res_path
        self.label_file_name = label_file_name
        self.answer_dirs = answer_dirs
        self.label_p_dir_name = label_p_dir_name
        self.appoint_dir_tree = appoint_dir_tree
        # self.pixel_range_path = pixel_range_path

    def write_result(self, file_path, content):
        if FileOpUtil.write_result(file_path, content):
            exit()
        else:
            raise Exception("无法将指定内容写入指定文件中")

    # 判断选手提交作品解压后第一级目录是否正确，正确判断目录名是否符合预期，如果不符合，目录重命名
    def check_submit_dir(self, p_dir, expect):
        res = None
        tmp = os.listdir(p_dir)
        if expect not in tmp:
            # msg = ErrorCode.LabelDirExpectDirNotFound.value + ";".join(tmp)
            msg = ErrorCode.LabelDirExpectDirNotFound.value
            res = {"status": "failed", "errorCode": ErrorCode.LabelFileErrorCode.value,  "errorMessage": msg+"：期望解压后一级目录为："+str(expect)+\
                                                                                                        "，提交作品解压后一级目录为： "+str(tmp[0]),
                   "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
        return res

    # 解压文件
    def unzip_file(self, abs_srcfile_path, abs_dest_dir):
        res = None
        try:
            zf = zipfile.ZipFile(abs_srcfile_path)
            zf.extractall(path=abs_dest_dir)
            zf.close()
        except zipfile.BadZipFile as zipE:
            res = {"status": "failed", "errorCode": ErrorCode.LabelFileErrorCode.value,
                   "errorMessage": ErrorCode.LabelFileIsNotZip.value+"：提交作品格式为： "+str(abs_srcfile_path.split(".")[-1]), "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
        except Exception as e:
            res = {"status": "failed", "errorCode": ErrorCode.SystemErrorCode.value,
                   "errorMessage": e.__str__(), "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
        return res

    # 判断评分结果路径的父目录是否存在，不存在尝试创建，如果不能创建，退出评分，并提示系统问题
    def is_result_dir(self):
        try:
            p_dir = os.path.dirname(self.score_res_path)
            if not os.path.isdir(p_dir):
                os.makedirs(p_dir)

            if not os.path.isfile(self.score_res_path):
                f = open(self.score_res_path, 'w')
                f.close()

            return {"status": "succeed"}
        except Exception as e:
            return {"status": "failed", "errorCode": ErrorCode.SystemErrorCode.value, "errorMessage": e.__str__(),
                    "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}

    def delete_result_path(self):
        if os.path.isfile(self.score_res_path):
            try:
                os.remove(self.score_res_path)
            except Exception as e:
                raise Exception(e.__str__())

    # 判断文件名后缀是不是zip
    def file_suffix(self):
        return self.label_file_name.endswith(".zip")

    def fun(self):
        score_action_dir_format = self.score_action_dir.replace("\\", "/")
        # print(score_action_dir_format) #D:/python_tensorflow_mars/Competition_2021/evaluate_result

        label_path = FileOpUtil.join_paths(score_action_dir_format, self.label_file_name)
        # print(label_path) #D:/python_tensorflow_mars/Competition_2021/evaluate_result/result.zip

        zip_dir_path = FileOpUtil.join_paths(score_action_dir_format, 'zip_file')
        # print(zip_dir_path) #D:/python_tensorflow_mars/Competition_2021/evaluate_result/zip_file

        # 确认结果文件是否存在，存在则删除。
        self.delete_result_path()

        # 确认标签评分结果文件是否可以读写，不能则抛出异常，结束评分
        check_result_dir = self.is_result_dir()
        if check_result_dir["status"] == "failed":
            raise Exception(check_result_dir["errorMessage"])

        # 确认图片像素文件存在并且可以加载
        # images_pixel_range = self.load_images_pixel_range()

        # 确认标签文件存在，不存在将结果写入评分结果，结束评分
        if os.path.isdir(label_path):
            content = {"status": "failed", "errorCode": ErrorCode.SystemErrorCode.value,
                       "errorMessage": ErrorCode.LabelFileIsDir.value, "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
            self.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
        else:
            if not os.path.isfile(label_path):
                content = {"status": "failed", "errorCode": ErrorCode.SystemErrorCode.value,
                           "errorMessage": ErrorCode.LabelFileNotExists.value,"scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
                self.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))

        # 删除已经存在的用于解压标签的目录，如果异常，抛出异常，结束评分
        try:
            if os.path.isdir(zip_dir_path):
                shutil.rmtree(zip_dir_path)
            elif os.path.isfile(zip_dir_path):
                os.remove(zip_dir_path)
        except Exception as e:
            content = {"status": "failed", "errorCode": ErrorCode.SystemErrorCode.value, "errorMessage": e.__str__(),
                       "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
            self.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))

        # 重新创建用于解压标签的目录
        if not os.path.exists(zip_dir_path):
            os.makedirs(zip_dir_path)

        # =====================================下面逻辑需要将结果记录到结果中=====================================
        print("#############判断是否是zip后缀#############")
        # print(self.file_suffix())
        if self.file_suffix() is False:
            content = {"status": "failed","scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}, "errorCode": ErrorCode.LabelFileErrorCode.value,
                       "errorMessage": ErrorCode.LabelFileIsNotZip.value}
            FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
            if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
                raise Exception("can not save result into target file")
            exit()

        print("#############判断压缩文件名是否是result#############")
        # print('标签文件名：',self.label_file_name)
        # if self.label_file_name == "result.zip":
        #     pass
        # else:
        #     content = {"status": "failed", "result": 0, "errorCode": ErrorCode.LabelFileErrorCode.value,
        #                "errorMessage": ErrorCode.LabelFileName.value}
        #     FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
        #     if not FileOpUtil.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False)):
        #         raise Exception("can not save result into target file")
        #     exit()

        # 文件解压失败，记录失败原因，退出程序
        # print("#############解压文件#############")
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        unzip_res = self.unzip_file(label_path, zip_dir_path)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # print(unzip_res)
        if unzip_res is not None:
            # print(unzip_res)
            self.write_result(self.score_res_path, json.dumps(unzip_res, ensure_ascii=False))


        # 解压后的文件不符合要求，记录原因，退出程序
        label_dir_format = self.check_submit_dir(zip_dir_path, self.label_p_dir_name)
        if label_dir_format is not None:
            # print(label_dir_format)
            self.write_result(self.score_res_path, json.dumps(label_dir_format, ensure_ascii=False))

        submit_dir_path = zip_dir_path

        check_dir_format = CheckSubmitDirFormat(self.appoint_dir_tree, submit_dir_path)
        check_dir_format_res = check_dir_format.check_dir_format()
        # print(json.dumps(check_dir_format_res, ensure_ascii=False))

        format_state = check_dir_format_res["state"]
        if format_state == "failed":
            # 退出评分脚本，将结果写入到脚本，记录退出原因
            content = {"status": "failed", "errorCode": ErrorCode.LabelFileErrorCode.value,
                       "errorMessage": ErrorCode.LabelNoEffectiveDirs.value, "scoreObject":{"PAScore": 0,"Top_1_Error":0, "score": 0}}
            self.write_result(self.score_res_path, json.dumps(content, ensure_ascii=False))
        # else:
        #     return check_dir_format_res

        return {"check_dir_format_res": check_dir_format_res}

