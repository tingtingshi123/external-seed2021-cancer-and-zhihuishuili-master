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


class Top_1_Error(object):
    def __init__(self, answer_file, real_submit_label):
        self.answer_file = answer_file  # 答案标签
        self.real_submit_label = real_submit_label  # 命中标签


    # @MonitorUtil.func_time
    def top_1_error(self,answer_file, real_submit_label): # 对两个文件中图片标签计算
        concat_label = pd.merge(answer_file, real_submit_label, right_on='image_name', left_on='image_name', how='left'
                                , suffixes = ['_answer', '_submit'])
        p = 0
        for i in range(len(concat_label)):
            # print(concat_label.loc[i,'label_answer'],concat_label.loc[i,'label_submit'])
            if (str(concat_label.loc[i,'label_answer'])==concat_label.loc[i,'label_submit'])\
                    or (concat_label.loc[i,'label_answer']==concat_label.loc[i,'label_submit']):
                p+=0
            else:
                p+=1
        return p



    # @MonitorUtil.func_time
    def fun(self):
        submit_files_num = len(self.real_submit_label)
        counts = len(self.answer_file)
        if submit_files_num == 0:
            tmp_score = 1 # 如果提交为空，错误为1
        else:
            p = self.top_1_error(self.answer_file, self.real_submit_label)
            # print("标签错误个数：",p)
            tmp_score=p/counts
        return tmp_score

