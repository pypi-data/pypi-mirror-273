# -*- coding: UTF-8 –*-
import getpass
import os
import pathlib
import platform
import subprocess
from bypy import ByPy
from concurrent.futures import ThreadPoolExecutor


class BaiDu:
    """
    upload2baidu: 按文件夹上传时, 可以直接调用
    upload_as_file: 逐个文件上传, 必须先实例化, 再运行
    如果通过调用命令行终端运行, 云端路径必须使用linux格式，不要使用windows格式,否则在windows系统里面会上传失败(无法在云端创建文件)
    """
    def __init__(self):
        pass

    @staticmethod
    def upload2baidu(_up_load_path, _remotepath, _delete_file=False):
        """
        如果通过调用命令行终端运行, 云端路径必须使用linux格式，不要使用windows格式,否则在windows系统里面会报错
        _up_load_path: 将此目录上传文件到云端
        从本地_up_load_path 保存在云端的文件夹 _remotepath
        _delete_file : 上传文件后是否删除原文件
        suffix: 需要同步的文件后缀, 列表, 必传
        """
        _up_load_path = str(_up_load_path)
        _remotepath = str(_remotepath)
        if not os.path.exists(_up_load_path):
            print(f'{_up_load_path}: 本地目录不存在，没有什么可传的')
        print(f'正在上传百度云...')
        if platform.system() == 'Windows':
            bp = ByPy()
            bp.upload(localpath=str(_up_load_path), remotepath=str(_remotepath))  # 上传文件到百度云
        else:
            command = f'bypy upload "{str(_up_load_path)}" "{str(_remotepath)}" --on-dup skip'  # 相同文件跳过
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(e)

        if _delete_file:
            for root, dirs, files in os.walk(_up_load_path, topdown=False):
                for name in files:
                    if 'ini' not in name:
                        os.remove(os.path.join(root, name))
            print(f'已删除{_up_load_path}文件内容')
        print(f'上传完成～')

    def upload_as_file(self, _up_load_path, _remotepath, suffix: list, _delete_file=False):  # 逐个文件上传
        _up_load_path = str(_up_load_path)
        _remotepath = str(_remotepath)
        upload_infos = []
        for root, dirs, files in os.walk(_up_load_path, topdown=False):
            for name in files:
                if 'ini' in name or 'desktop' in name or '.DS_Store' in name:
                    continue
                for suf in suffix:
                    if suf in name:
                        upload_infos += [[os.path.join(root, name), f'{_remotepath}/{name}']]

        with ThreadPoolExecutor() as pool:  # 线程池
            pool.map(self.uploads, upload_infos)
        if _delete_file:
            for root, dirs, files in os.walk(_up_load_path, topdown=False):
                for name in files:
                    if 'ini' not in name:
                        os.remove(os.path.join(root, name))
            print(f'已删除{_up_load_path}文件内容')
        print(f'上传完成～')

    def upload_single_file(self, _up_file, _remote_file, _delete_file=False):  # 逐个文件上传
        _up_file = str(_up_file)
        _remote_file = str(_remote_file)
        self.uploads([_up_file, _remote_file])
        if _delete_file:
            os.remove(_up_file)


    @staticmethod
    def uploads(upload_info):  # 逐个文件上传, 被调用函数
        _up_load, _remote = upload_info
        _up_load = str(_up_load)
        _remote = str(_remote)
        if platform.system() == 'Windows':
            bp = ByPy()
            bp.upload(localpath=_up_load, remotepath=_remote)  # 上传文件到百度云
        else:
            command = f'bypy upload "{_up_load}" "{_remote}" --on-dup skip --chunk 1MB'  # 相同文件跳过
            try:
                subprocess.run(command, shell=True)
                print(os.path.basename(_up_load))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print(1)
