import cv2
import json
import pandas as pd
import numpy as np
from utils.MonitorUtil import MonitorUtil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.Fileoputil import FileOpUtil
import os
from PIL import Image


class PAScore(object):
    def __init__(self, answer_file_kv, real_hit_jpg_kv):
        self.answer_file_kv = answer_file_kv  # 答案
        # self.real_submit_png_kv = real_submit_png_kv
        self.real_hit_jpg_kv = real_hit_jpg_kv  # 命中
        # self.potential_hit = potential_hit

    # @MonitorUtil.func_time
    def one_file(self,image1,image2): # 对两个图片像素值计算
        """

        :param image1: 图片地址1（答案）
        :param image2: 图片地址2 (提交)
        :return: 图片对比的准确度
        """
        acc = 0
        try:
            gray1 = np.array(Image.open(image1))  # py2.x
            gray2 = np.array(Image.open(image2))
            size = gray1.size  # 答案尺寸
            diff = np.mat(gray2) - np.mat(gray1)
            k = pd.DataFrame(diff)
            acc += np.sum((k == 0).astype(int).sum())/size
            # print(acc)
        except:
            acc = 0
        return acc

    # @MonitorUtil.func_time
    def pa_serial(self):  # 单线程总得分
        count = len(self.answer_file_kv.keys())  # 答案个数
        scores = []  # 得分
        filename1 = list(self.real_hit_jpg_kv.keys())  # 真实命中的文件名
        filename2 = list(self.answer_file_kv.keys())  # 答案文件名
        if len(filename1) > 0:
            for filename in filename1:
                if filename in filename2:
                    score = self.one_file(self.answer_file_kv[filename], self.real_hit_jpg_kv[filename])  # 每个图片得分
                    scores.append(score)

                else:
                    score = 0
                    scores.append(score)
        else:
            scores = 0
        return np.sum(scores) / count  # 直接得出总准确率

    # @MonitorUtil.func_time
    def pa_parallel(self, index_range):  #多线程总得分
        filename1 = list(self.real_hit_jpg_kv.keys())  # 真实命中的文件名
        filename2 = list(self.answer_file_kv.keys())  # 答案文件名
        start = index_range["start"]
        end = index_range["end"]
        scores = []  # 保存每组得分
        # print(filename1)  # ['3000', '3001', '3002', '3003', '']
        for i in range(start, end):
            # print(i)  # 0
            # print(filename1[i])
            # if len(filename1[i]) > 0:
            if filename1[i] in filename2:
                score = self.one_file(self.answer_file_kv[filename1[i]], self.real_hit_jpg_kv[filename1[i]])  # 每个图片得分
                scores.append(score)
            else:
                score = 0
                scores.append(score)
            # else:
            #     score = 0
            #     scores.append(score)   # 得出每个图片的准确率
        return scores

    # @MonitorUtil.func_time
    def pa_concurrently(self, split_size, max_workers_num):  # 多线程
        scores = []
        split_ = FileOpUtil.split_files(self.real_hit_jpg_kv, split_size)
        # print(split_)  # [{'start': 0, 'end': 200}, {'start': 200, 'end': 400}, {'start': 400, 'end': 600}]
        with ProcessPoolExecutor(max_workers=max_workers_num) as t:
            threads = []
            for i in split_:
                # print('i',i)  # i {'start': 0, 'end': 200}
                thread = t.submit(self.pa_parallel, i)  # 多线程
                threads.append(thread)
            for j in as_completed(threads):

                scores = scores + j.result()
        if len(scores) > 0:
            return np.array(scores)   # 多线程每个图片的准确率
        else:
            return 0

    # @MonitorUtil.func_time
    def fun(self):
        submit_files_num = len(self.real_hit_jpg_kv)
        counts = len(self.answer_file_kv)
        if counts == 0:
            tmp_score = 0
        else:
            if submit_files_num > 5:  # 并行
                tmp_score = self.pa_concurrently(5, 6)   # 每个文件的准确率
                # print(tmp_score)
                tmp_score = np.sum(tmp_score) / counts  # 所有文件的平均准确率
            else:
                tmp_score = self.pa_serial()  # 串行

        return tmp_score

