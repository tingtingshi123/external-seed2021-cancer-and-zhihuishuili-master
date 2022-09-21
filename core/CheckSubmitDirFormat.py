from utils.Fileoputil import FileOpUtil


class CheckSubmitDirFormat(object):
    def __init__(self, appoint_dir_tree, submit_dir_path):
        """
        :param appoint_dir_tree: list
        :param submit_dir_path: str
        """
        self.submit_dir_path = submit_dir_path
        self.appoint_dir_tree = appoint_dir_tree

    # 将目录转换成指定格式，业务相关逻辑
    def transfer_dir_format(self, dir_list, abs_parent_dir):
        source_data = []
        lower_data = []

        for i in dir_list:
            sub_dir = i.replace(abs_parent_dir, "").replace("\\", "/")
            lower_dir = sub_dir.lower()
            lower_data.append(lower_dir)
            tmp_dict = {"source_dir": sub_dir, "lower_dir": lower_dir}
            source_data.append(tmp_dict)
        return {"dir_src_dest": source_data, "dir_dest": lower_data}

    # 判断选手作品文件目录是否有缺失，如果全部缺失，则校验状态置为failed，如果有一个存在状态置为succeed，缺失的文件目录记录下来
    def get_submit_lack_dirs(self, appoint_dir_src_dest, submit_dir_dest):
        submit_lack_dir = []
        for i in appoint_dir_src_dest:
            appoint_source_dir = i["source_dir"]
            appoint_lower_dir = i["lower_dir"]

            if appoint_lower_dir not in submit_dir_dest:
                submit_lack_dir.append(appoint_source_dir)
        return submit_lack_dir

    def get_submit_hit_dirs(self, submit_dir_src_dest, appoint_dir_dest):
        submit_effective_dirs = []
        submit_ineffective_dirs = []
        for i in submit_dir_src_dest:
            submit_source_dir = i["source_dir"]
            submit_lower_dir = i["lower_dir"]
            if submit_lower_dir in appoint_dir_dest:
                abs_path = self.submit_dir_path.replace("\\", "/") + submit_source_dir
                if not FileOpUtil.is_dir_empty(abs_path):
                    submit_effective_dirs.append(abs_path)
                else:
                    submit_ineffective_dirs.append(submit_source_dir)
        return {"submit_effective_dirs": submit_effective_dirs, "submit_ineffective_dirs": submit_ineffective_dirs}

    # 判断选手作品文件目录多出来的目录，记录多出来的文件目录
    def get_submit_extra_dirs(self, submit_dir_src_dest, appoint_dir_dest):
        submit_extra_dirs = []
        for j in submit_dir_src_dest:
            submit_source_dir = j["source_dir"]
            submit_lower_dir = j["lower_dir"]

            if submit_lower_dir not in appoint_dir_dest:
                submit_extra_dirs.append(submit_source_dir)
        return submit_extra_dirs

    # 判断选手上传的文件目录是否符合要求
    def check_dir_format(self):
        check_ = {}
        submit_sub_dirs = []
        print("约定的目录结构：")
        print(self.appoint_dir_tree)
        appoint_dir_format = self.transfer_dir_format(self.appoint_dir_tree, "")
        print("约定的目录结构格式化结果：")
        print(appoint_dir_format)

        FileOpUtil.get_subdir(self.submit_dir_path, submit_sub_dirs)
        print("用户提交的作品子目录结构：")
        print(submit_sub_dirs)

        if len(submit_sub_dirs) > 0:
            submit_dir_format = self.transfer_dir_format(submit_sub_dirs, self.submit_dir_path)
            print("用户提交的作品目录结构格式化结果：")
            print(submit_dir_format)

            appoint_dir_src_dest = appoint_dir_format["dir_src_dest"]
            appoint_dir_dest = appoint_dir_format["dir_dest"]
            submit_dir_src_dest = submit_dir_format["dir_src_dest"]
            submit_dir_dest = submit_dir_format["dir_dest"]

            extra_dirs = self.get_submit_extra_dirs(submit_dir_src_dest, appoint_dir_dest)
            hit_dirs = self.get_submit_hit_dirs(submit_dir_src_dest, appoint_dir_dest)
            print("多出的：")
            print(extra_dirs)
            print("命中目录：")
            print(hit_dirs)
            hit_num = len(hit_dirs)
            appoint_dirs_num = len(self.appoint_dir_tree)
            # 判断提交作品满足要求的目录有哪些，少了哪些
            submit_effective_dirs = hit_dirs["submit_effective_dirs"]
            submit_ineffective_dirs = hit_dirs["submit_ineffective_dirs"]
            effective_dirs_num = len(submit_effective_dirs)
            ineffective_dirs_num = len(submit_ineffective_dirs)
            if effective_dirs_num == 0:
                check_["state"] = "failed"
            else:
                check_["state"] = "succeed"
                check_["effective_dirs"] = submit_effective_dirs
            if ineffective_dirs_num > 0:
                check_["ineffective_dirs"] = submit_ineffective_dirs
            lack_dirs = self.get_submit_lack_dirs(appoint_dir_src_dest, submit_dir_dest)
            print("缺少目录：")
            print(lack_dirs)
            if len(lack_dirs) > 0:
                check_["lack_dirs"] = lack_dirs

            if len(extra_dirs) > 0:
                check_["extra_dirs"] = extra_dirs
        else:
            check_["state"] = "failed"
        return check_
