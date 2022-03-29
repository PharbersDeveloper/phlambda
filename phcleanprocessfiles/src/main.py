from utils.cleanexpiredfile import CleanExpiredFile, SearchFilesPath


base_path = "/mnt/tmp"
# 运行指定dag
def lambda_handler(event, context):
    waitting_clean_dirs = SearchFilesPath(base_path).handle_base_path()
    #--指定目录
    for dir in waitting_clean_dirs:
        clean_file = CleanExpiredFile(dir)
        #--过期时间 单位h
        clean_file.clean_expired_files(24)
