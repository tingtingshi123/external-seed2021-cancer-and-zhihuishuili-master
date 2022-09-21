import os


class GetFilesInfo(object):
    """
    获取比赛所用数据集和答案相关文档。具有业务属性，无法通用，跟着比赛走
    """
    def __init__(self):
        pass

    @staticmethod
    def focusight_get_file_name(dir_path):
        res = []
        try:
            files = os.listdir(dir_path)
            for i in files:
                file_path = dir_path.replace("\\", "/") + "/" + i
                if os.path.isfile(file_path):
                    file_name = i.split(".")[0]
                    res.append(file_name)
        except Exception as e:
            print(e)
        return res
