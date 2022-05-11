def upload_files(conf):
    conf.get("s3").upload_dir(
        dir=conf.get("jobPath"),
        bucket_name=conf.get("bucket"),
        s3_dir=conf.get("cliVersion") + conf.get("dagS3JobsPath") + conf.get("name") + "/" + conf.get("jobFullName")
    )
