from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#统计各个类别的TP、FP、FN、TN，分别计算各自的Precision和Recall，得到各自的F1值，然后取平均值得到Macro-F1
class F1_score():
    def __init__(self,real_submit,answer):
        self.real_submit=real_submit
        self.answer=answer

    def get_onehot(self,real_submit,answer):
        real_submit_dummies=pd.get_dummies(real_submit,columns=["label"],prefix='submit')
        answer_dummies=pd.get_dummies(answer,columns=["label"],prefix='answer')
        concat_label= pd.merge(answer_dummies, real_submit_dummies,right_on='image_name',left_on='image_name',how='left')
        # print('合并后的列名；',concat_label.columns.tolist())
        # 答案列名
        y_true=concat_label[[name for name in concat_label.columns.tolist() if name.startswith('answer_')]]
        y_true=y_true[['answer_0', 'answer_1', 'answer_2', 'answer_3']]
        # 提交列名
        y_hat=concat_label[[name for name in concat_label.columns.tolist() if name.startswith('submit_')]]
        # 更改列名（如果含有浮点数）
        y_hat.rename(columns={x: x.split('.')[0] for x in y_hat},inplace=True)
        # print('更改后列名：',y_hat.columns.tolist())
        # 找到缺失的类别
        submit_label = [i.split("_")[1] for i in y_hat.columns.tolist()]
        answer_label = [i.split("_")[1] for i in y_true.columns.tolist()]
        # print(submit_label, answer_label)
        if submit_label!=answer_label:
            # 提交的结果中缺失的类别
            # lostnum = [i for i in answer_label if i not in submit_label][0]
            lostnum=[i for i in answer_label if i not in submit_label]
            print('缺失类型：',lostnum)
            names=[('submit_'+i) for i in lostnum]
            # print(names)
            y_hat=pd.concat([pd.DataFrame(np.zeros(shape=(len(y_hat),len(names))),columns=names),y_hat],axis=1)
            # print(y_hat)
        else:
            y_hat=y_hat
        # 提交按指定位置排列列名
        y_hat=y_hat[['submit_0', 'submit_1', 'submit_2', 'submit_3']].fillna(0)
        # print('预测：',y_hat)
        y_true=np.array(y_true)
        y_hat=np.array(y_hat)
        return y_hat,y_true

    def f1(self):
        '''
        y_hat是未经过sigmoid函数激活的
        输出的f1为Marco-F1
        '''
        y_hat,y_true=self.get_onehot(self.real_submit,self.answer)

        epsilon = 1e-7
        tp = np.sum(y_hat * y_true, axis=0)
        fp = np.sum(y_hat * (1 - y_true), axis=0)
        fn = np.sum((1 - y_hat) * y_true, axis=0)
        # print('每个类别错误预测为正的个数：',fp,'\n每个类别正确预测为正的个数：',tp,'\n每个类别错误预测为负的个数：',fn)
        p = tp / (tp + fp + epsilon)  # epsilon的意义在于防止分母为0，否则当分母为0时python会报错
        r = tp / (tp + fn + epsilon)
        # print('每个类别的精确率：',p,'\n每个类别的召回率：',r)
        f1 = 2 * p * r / (p + r + epsilon)
        f1 = np.where(np.isnan(f1), np.zeros_like(f1), f1)
        # print('每个类别的f1得分：',f1)
        return round(np.mean(f1),4)
