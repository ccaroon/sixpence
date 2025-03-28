import os
import tarfile

from utils.date_helper import DateHelper

# https://docs.python.org/3/library/archiving.html
class Archive:
    def __init__(self, path):
        # path = /home/smith/backup/Sixpense/sixpence.tgz

        # /home/smith/backup/Sixpence | sixpence.tgz
        (dir_name, file_name) = os.path.split(path)

        # sixpence | .tgz
        (file_base, file_ext) = os.path.splitext(file_name)

        self.__base_path = dir_name
        self.__file_base = file_base

        os.makedirs(self.__base_path, exist_ok=True)

        # /home/smith/backup/Sixpense/sixpence-YYYYMMDD_HHmmss.tgz
        dt_stamp = DateHelper.now().format("YYYYMMDD_HHmmss")
        self.__path = f"{self.__base_path}/{self.__file_base}-{dt_stamp}{file_ext}"

        self.__items = []


    def add(self, name):
        """Add a new file or directory to the Archive"""
        self.__items.append(name)


    def write(self):
        with tarfile.open(self.__path, "x:gz", ) as tf:
            for item in self.__items:
                tf.add(item)


    def clean(self, older_than):
        """Clean up the Archive"""
        cut_off_date = DateHelper.now().shift(days=older_than * -1)

        for _, _, files in os.walk(self.__base_path):
            for file in files:
                if file.startswith(self.__file_base):
                    file_path = os.path.join(self.__base_path, file)
                    mtime = os.path.getmtime(file_path)
                    file_date = DateHelper.as_arrow(mtime)
                    if file_date < cut_off_date:
                        os.remove(file_path)
