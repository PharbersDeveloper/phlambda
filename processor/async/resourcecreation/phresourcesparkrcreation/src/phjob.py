def create_ph_job_file(conf):
    file_lines = conf.get("s3").open_object_by_lines(conf.get("bucket"),
                                                     conf.get("cliVersion") + conf.get("templatePhjobFile"))

    with open(f"{conf.get('jobPath')}/phjob.R", "w") as file:
        for line in file_lines:
            line = line + "\n"
            if "# $alfred_data_frame_input" in line:
                input_item = "\n".join(list(map(lambda item: f"""\tdata_frame <- cmd_args$df_{item}""",
                                                conf.get("inputs"))))
                file.write(input_item + "\n")
            else:
                file.write(line)
