def upload_files(conf):
    # dag_s3_jobs_path = os.environ["DAG_S3_JOBS_PATH"] #"/jobs/python/phcli/"

    conf.get("s3").upload_dir(
        dir=conf.get("jobPath"),
        bucket_name=conf.get("bucket"),
        s3_dir=conf.get("cliVersion") + conf.get("dagS3JobsPath") + \
               conf.get("dagName") + "/" + conf.get("jobDisplayName")
    )
