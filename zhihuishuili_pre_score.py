import sys
from core.SeedScore_zhihuishuili_pre import SeedScore
import time,datetime
from core.error_code import ErrorCode
from utils.Fileoputil import FileOpUtil
import json,io
# ROOT_DIR = r"D:\python_tensorflow_mars\Competition_2021\external-seed2021-cancer-zhuihuishuili"  # 整个评分的项目脚本
ROOT_DIR = "/opt/score-script"
sys.path.append(ROOT_DIR)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    score_action_dir = sys.argv[1] # 选手提交结果路径
    # print(score_action_dir)
    score_res_path = sys.argv[2] # 日志路径包括日志文件result.json
    # print(score_res_path)
    label_file_name = sys.argv[3] # 压缩包
    answer_dirs = [r"/data/competition/2021/seed_zhihuishuili/true"]  # 答案地址

    # answer_dirs = [r"D:\python_tensorflow_mars\Competition_2021\evaluate_result_zhihuishuili\result\true"]  # 答案地址

    appoint_dir_tree = [r"/result"]  # 提交的压缩文件名称 zip_file下一层目录  约定的目录结构

    coordinate_start = 0  # 初始化标签值为0（坐标范围从0-2047）
    compatible_file_suffix = ""  # 固定文件格式 此处png
    label_p_dir_name = "result"  # 提交结果字典名称

    score = SeedScore(score_action_dir, score_res_path, label_file_name, answer_dirs,  coordinate_start,
                  compatible_file_suffix, label_p_dir_name, appoint_dir_tree)
    score.fun()


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    diff = (end - start).seconds
    # print("The function run time is : %.05f seconds" % diff)
    if diff > 90:
        score_res_path = sys.argv[2]
        content = {"status": "failed", "result": 0,
                   "errorCode": ErrorCode.TimeOutCode.value,
                   "errorMessage": ErrorCode.TimeOutMsg.value}
        FileOpUtil.write_result(score_res_path, json.dumps(content, ensure_ascii=False))
        if not FileOpUtil.write_result(score_res_path,
                                       json.dumps(content, ensure_ascii=False)):
            raise Exception("can not save result into target file")
        exit()
