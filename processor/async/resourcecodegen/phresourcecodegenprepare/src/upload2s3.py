def upload_file(conf):
    file_name = "phjob.py"
    local_path = f"{conf.get('jobPath')}/{file_name}"
    s3_path = f"""{conf.get("cliVersion")}{conf.get("dagS3JobsPath")}{conf.get("name")}/{conf.get("jobFullName")}/{file_name}"""
    conf.get("s3").upload(local_path, conf.get("bucket"), s3_path)
