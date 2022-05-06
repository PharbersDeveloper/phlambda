
def create_ph_main_file(conf):
    # template_phmain_file = os.environ["TM_PHMAIN_FILE"] # 环境变量 "/template/python/phcli/maxauto/phmain-r_dev.tmp"

    runtime = "r"

    file_lines = conf.get("s3").open_object_by_lines(conf.get("bucket"),
                                                     conf.get("cliVersion") + conf.get("templatePhmainFile"))

    with open(f"{conf.get('jobPath')}/phmain.R", "a") as file:
        for line in file_lines:
            line = line + "\n"
            if line == "$alfred_debug_execute\n":
                file.write(f"""
args <- list(name="{conf.get("jobDisplayName")}")

inputs <- list({', '.join(['"' + input_item.get("name") + '"' for input_item in conf.get("inputs")])})
output <- "{conf.get("output")}"

project_id <- "{conf.get("projectId")}"
project_name <- "{conf.get("dagName")}"
runtime <- "{runtime}"

ph_conf <- fromJSON(input_args$ph_conf, simplifyVector=FALSE)

user_conf <- ph_conf$userConf

ds_conf <- as.list(ph_conf$datasets)

args <- c(args, user_conf)
args[["ds_conf"]] <- ds_conf
args <- c(args, input_args)

output_version <- paste(args$run_id, "_", ph_conf$showName, sep="")

df_map <- create_input_df(runtime, inputs, args, project_id, project_name, output_version)

args <- c(args, df_map)

result <- exec(args)

args <- c(args, result)

create_outputs(runtime, args, ph_conf, output, project_id, project_name, output_version)
                """)
            else:
                file.write(line)
