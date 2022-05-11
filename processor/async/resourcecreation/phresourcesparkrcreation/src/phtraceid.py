import subprocess


def create_ph_trace_id_file(conf):
    subprocess.call(["touch", conf.get("jobPath") + "/" + conf.get("traceId")])
