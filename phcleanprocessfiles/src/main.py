import os

from utils.cleanexpiredfile import CleanExpiredFile, SearchFilesPath


# 运行指定dag
def lambda_handler(event, context):

    base_path = os.getenv("BASE_PATH")
    expired_time = os.getenv("EXPIRED_TIME")
    waitting_clean_dirs = SearchFilesPath(base_path).handle_base_path()
    #--指定目录
    for dir in waitting_clean_dirs:
        clean_file = CleanExpiredFile(dir)
        #--过期时间 单位h
        clean_file.clean_expired_files(expired_time)
