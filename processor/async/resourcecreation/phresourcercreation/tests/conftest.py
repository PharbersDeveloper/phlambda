import os

os.environ["BUCKET"] = "ph-platform"
os.environ["CLI_VERSION"] = "2020-11-11"
# os.environ["JOB_PATH_PREFIX"] = "/tmp/phjobs/"
os.environ["JOB_PATH_PREFIX"] = "/Users/qianpeng/Desktop/TestCreateFIle/"
os.environ["TM_PHMAIN_FILE"] = "/template/python/phcli/maxauto/phmain-r_dev.tmp"
os.environ["TM_PHJOB_FILE"] = "/template/python/phcli/maxauto/phjob-r_dev.tmp"
os.environ["DAG_S3_JOBS_PATH"] = "/jobs/python/phcli/"
