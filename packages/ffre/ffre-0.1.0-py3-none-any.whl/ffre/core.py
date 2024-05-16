import os
import re
import numpy as np

"""
该部分代码旨在搜索目标目录下的特定文件

1. 使用os.walk遍历目标路径下的所有文件，并记录: 
    目标后缀 && fname符合pattern && fname不符合exclude && ftype符合tpattern && ftype不符合texclude 
    && 满足条件function(rel_dir, fname, ftype) -> True
到FCollect对象

2. 在FCollect中，类似列表的方式储存收集到的fpath信息，因此可以直接迭代

"""


class FCollect:
    """
    该类用于对搜索结果进行汇总
    """

    def __init__(self, root_path: str, ndarray_data: np.ndarray):
        """

        :param root_path:
        :param ndarray_data: relpath, fname, ftype
        """
        self.root_path = os.path.abspath(root_path)
        self.data = ndarray_data

    def __str__(self):
        return f"<{self.__class__.__name__} root={self.root_path}>\n" + str(self.data)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.__iteration__()

    def __iteration__(self):
        for rel_path, fname, ftype in self.data:
            yield os.path.join(self.root_path, rel_path, fname + ftype)


class DirExistsError(Exception):
    pass


class UserFunctionException(Exception):
    pass


class FileFinder:
    def __init__(self, target_path: str, default_types=()):
        if target_path == '':
            target_path = os.getcwd()
        self.dir = target_path  # 搜索的起点位置
        self.dftypes = self._types_format(*default_types)  # 指定默认搜索类型

        # 检查路径是否合理
        if not os.path.exists(target_path):
            raise DirExistsError(f"Target directory is not exists -: {target_path}")
        if not os.path.isdir(target_path):
            raise NotADirectoryError(f"Target path is not a directory -: {target_path}")

    @staticmethod
    def _types_format(*types):
        new_types = []
        for _t in types:
            _t = _t.lower()
            if _t[0] != '.':
                _t = '.' + _t
            new_types.append(_t)
        return new_types

    @staticmethod
    def _match_fnametype(
            fnametype:str,
            *looking_for_types,
            pattern: str = None,
            exclude: str = None,
            tpattern: str = None,
            texclude: str = None
    ) -> bool:
        """
        判断目标文件的名称和后缀是否满足特定条件
        """

        fname, ftype = os.path.splitext(fnametype)
        if ftype.lower() in looking_for_types:
            flag = True
            if flag and pattern:
                flag = re.match(pattern, fname)

            if flag and exclude:
                flag = not re.match(exclude, fname)

            if flag and tpattern:
                flag = re.match(tpattern, ftype)

            if flag and texclude:
                flag = not re.match(texclude, ftype)

            return flag
        return False

    _last_log = []

    @property
    def log(self) -> str:
        # return self._last_log
        return '\n'.join(self._last_log)

    def _new_log(
            self,
            head_line:str,
            types:list,
            pattern: str = None,
            exclude: str = None,
            tpattern: str = None,
            texclude: str = None,
            function: callable = None
            ):

        msg = head_line + '\n' + '* Looking For - '
        for tp in types: msg += "*" + tp + ', '
        if types: msg = msg[:-2]
        msg += '\n'

        if pattern is not None or tpattern is not None:
            tmp = "Pattern"
            if pattern is None:
                msg += '* t' + tmp + ": '" + tpattern + "'"
            elif tpattern is None:
                msg += '* ' + tmp + ": '" + pattern + "'"
            else:
                msg += '* (t)' + tmp + ": '" + pattern + "', '" + tpattern + "'"
            msg += '\n'

        if exclude is not None or texclude is not None:
            tmp = "Exclude"
            if exclude is None:
                msg += '* t' + tmp + ": '" + texclude + "'"
            elif texclude is None:
                msg += '* ' + tmp + ": '" + exclude + "'"
            else:
                msg += '* (t)' + tmp + ": '" + exclude + "', '" + texclude + "'"
            msg += '\n'

        if function is not None:
            try:
                msg += '* Function: ' + function.__name__ + '\n'
            except:
                msg += '* Function: ' + str(function)

        if msg:
            self._last_log = [msg]
        else:
            self._last_log = []

    def _log(self, msg):
        self._last_log.append(msg)

    def find(self,
             *added_types,
             pattern: str = None,
             exclude: str = None,
             tpattern: str = None,
             texclude: str = None,
             function: callable = None
             ) -> FCollect:
        """
        在target_path下寻找特定类型的文件, 会递归搜索子目录
        :param added_types: 可以添加额外的类型, 加不加.都可以
        格式: --------- 文件名.后缀名 ---------
        :param pattern: str, 目标文件名的正则表达筛选
        :param exclude: str, 目标文件名的正则排除筛选
        :param tpattern: str, 目标后缀名的正则表达筛选
        :param texclude: str, 目标后缀名的正则排除筛选
        :param function: callable, 可以添加额外函数(rel_path:str, fname:str, ftype:str) -> bool 来判断某个路径是否为目标路径
        :return: FCollect
        """
        # Step 1: format type in types
        # Step 2: walk through with (t)pattern & (t)exclude & function
        # Step 3: build-up ndarray
        # --------------------
        # 1:
        types = self.dftypes.copy() + self._types_format(*added_types)
        log_head = f"----------------------| {self.__class__.__name__} Log ---------------------->:"
        self._new_log(log_head, types, pattern, exclude, tpattern, texclude, function)

        # 2、3:
        new_data = []
        self._log("Find start at.")
        for dirpath, dirnames, filenames in os.walk(self.dir):
            rel_path = os.path.relpath(dirpath, self.dir)
            self._log("Enter: " + rel_path)
            rel_path = '' if rel_path == '.' else rel_path
            for fnametype in filenames:
                fname, ftype = os.path.splitext(fnametype)
                if function:
                    try:
                        _ = function(rel_path, fname, ftype)
                        if not _:
                            self._log("* File: '" + fnametype + "' can not fit user function. Get:{" + str(_) + "}")
                            continue
                    except Exception as err:
                        raise UserFunctionException("Meet Error during call user function. Aborpt Finding.")

                if not self._match_fnametype(
                        fnametype, *types,
                        pattern=pattern,
                        exclude=exclude,
                        tpattern=tpattern,
                        texclude=texclude,
                    ):
                    self._log("* File: '" + fnametype + "' can not fit re.")
                    continue

                self._log("* Collect file: '" + fnametype + "'")
                new_data.append([rel_path, fname, ftype])

        return FCollect(self.dir, np.array(new_data))


if __name__ == '__main__':
    # Example
    example = 1
    if example == 1:
        ff = FileFinder(r"E:\2024.02.22环网柜巡检数据表")
        fdata: FCollect = ff.find('xls', 'xlsx', pattern='^10[kK][vV].*线', exclude=r'^~.*')
    elif example == 2:
        ff = FileFinder(r"C:\Users\Administrator\Desktop\安规练习题（已导入）")
        fdata: FCollect = ff.find('xls', 'xlsx')  # 寻找指定目录的特定格式的文件

    # print(fdata, ff.log, sep='\n')
    for item in fdata:
        print(item)
