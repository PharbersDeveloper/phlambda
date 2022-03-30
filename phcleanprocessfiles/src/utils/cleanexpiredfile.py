import os
from datetime import datetime, timedelta


class SearchFilesPath:
    def __init__(self, base_path):
        self.metal_key = ["airflow", "chdumps", "clickhouse"]
        self.base_path = base_path

    def handle_base_path(self):
        full_base_path = list(map(lambda x: os.path.join(self.base_path, x), [x for x in os.listdir(self.base_path) if x not in self.metal_key]))
        full_base_path = [os.path.join(x, "tmp") for x in full_base_path if os.path.isdir(x) and "tmp" in os.listdir(x)]
        print(full_base_path)
        return full_base_path


class DeltaTime:
    def __init__(self):
        self.current_time = datetime.now()
    def calculate_delta_time(self, expired_time):
        return self.current_time - timedelta(hours=float(expired_time))

class CleanExpiredFile:

    def __init__(self, target_path):
        self.target_path = target_path
        self.current_time = DeltaTime().current_time
        self.all_files = list(self.findAllFile(target_path))
        self.all_files_with_ctime = list(map(lambda x: (x, datetime.fromtimestamp(os.stat(x).st_ctime)), self.all_files))

    def findAllFile(self, base):
        for root, ds, fs in os.walk(base):
            for f in fs:
                fullname = os.path.join(root, f)
                yield fullname

    def findAllDir(self, base):
        for root, ds, fs in os.walk(base):
            for dir in ds:
                fulldir = os.path.join(root, dir)
                yield fulldir

    #--清除过期文件
    def clean_expired_files(self, expired_time):
        delta_expired_time = DeltaTime().calculate_delta_time(expired_time)
        for file, ctime in self.all_files_with_ctime:
            if ctime <= delta_expired_time:
                try:
                    os.remove(file)
                    print(f"{file} delete success ")
                except Exception as e:
                    print(e)
        #--删除空文件夹
        for dir in self.findAllDir(self.target_path):
            if not os.listdir(dir):
                try:
                    os.rmdir(dir)
                except Exception as e:
                    print(e)

