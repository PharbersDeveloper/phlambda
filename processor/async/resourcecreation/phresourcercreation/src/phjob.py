
def create_ph_job_file(conf):
    # template_phjob_file = os.environ["TM_PHJOB_FILE"] # 环境变量 "/template/python/phcli/maxauto/phjob-r_dev.tmp"

    conf.get("s3").download(conf.get("bucket"), conf.get("cliVersion") + \
                            conf.get("templatePhjobFile"), conf.get('jobPath') + "/phjob.R")
