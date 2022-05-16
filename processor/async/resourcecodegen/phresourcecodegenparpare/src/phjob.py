import subprocess
from handler.GenerateInvoker import GenerateInvoker


def create_ph_job_file(conf):
    subprocess.call(["mkdir", "-p", conf.get("jobPath")])

    with open(f"{conf.get('jobPath')}/phjob.py", "w") as file:
        steps = list(map(lambda item: item["expressions"], conf["steps"]))
        operator_code = GenerateInvoker().execute(steps)
        file.write(operator_code)
