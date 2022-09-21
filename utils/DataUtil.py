class DataUtil(object):
    def __init__(self):
        pass

    # 获取数据类型
    @staticmethod
    def get_data_type(class_info):
        return str(type(class_info)).replace("<class '", "").replace("'>", "")

    @staticmethod
    def str_replace(source_str, replace_str):
        replace_str_num = len(replace_str)
        i_suffix = source_str[-replace_str_num:]
        if i_suffix == replace_str:
            i_prefix = source_str[: -replace_str_num]
            return i_prefix
        else:
            return None

    @staticmethod
    def get_dict_key(dict_):
        res = []
        if len(dict_) > 0:
            for i in dict_:
                res.append(i)
        return res

    @staticmethod
    def target_value(key, k_v_dict, replace_str):
        value = None
        if key in k_v_dict:
            value = k_v_dict[key]
        else:
            pattern_num = len(replace_str)
            key_num = len(key)
            if key_num > pattern_num:
                key_prefix = DataUtil.str_replace(key, replace_str)
                if key_prefix in k_v_dict:
                    value = k_v_dict[key_prefix]
        return value
