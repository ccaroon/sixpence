import os
import shutil

from utils.date_helper import DateHelper

# NOTES & TODO:
# https://docs.python.org/3/library/archiving.html
# * [ ] Make interface more like creating & adding files/dirs to an Archive file
#   - new archive
#   - add files
#   - add dirs
#   - write
# * [ ] Use one of the built-in archive modules (above)
class Archive:
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("Path must be a directory.")

        self.path = path


    def add(self, src):
        """Add a new file or directory to the Archive"""
        if os.path.isdir(src):
            self._add_dir(src)
        elif os.path.isfile(src):
            self._add_file(src)
        else:
            raise ValueError("Unsupported Src Type or Invalid Path")


    def __build_dst_path(self, src):
        ds = DateHelper.now().format("YYYYMMDD_HHmm")
        src_file = os.path.basename(src)
        parts = os.path.splitext(src_file)
        dest = f"{self.path}/{parts[0]}-{ds}"

        # Add ext
        if parts[1]:
            dest += f"{parts[1]}"

        return dest


    def _add_dir(self, src):
        dst = self.__build_dst_path(src)
        shutil.make_archive(dst, 'zip', src)


    def _add_file(self, src):
        dst = self.__build_dst_path(src)
        shutil.copyfile(src, dst)


    def files(self):
        return os.listdir(self.path)


    def remove(self, filename):
        file_path = os.path.join(self.path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


    def clean(self, prefix, older_than):
        """Clean up the Archive"""
        cut_off_date = DateHelper.now().shift(days=older_than * -1)

        for file in self.files():
            if file.startswith(prefix):
                mtime = os.path.getmtime(os.path.join(self.path, file))
                file_date = DateHelper.as_arrow(mtime)
                if file_date < cut_off_date:
                    self.remove(file)
