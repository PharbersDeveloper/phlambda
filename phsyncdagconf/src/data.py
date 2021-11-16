dag               dagconf

projectId   -->   projectId
representId -->   随机生成
cat         -->   if inputs,outputs == job else dataset
cmessage    -->   inputs,outputs,sourceId,targerId
ctype       -->   link if cmessage.get(inputs, outputs) == None else node
name        -->   flow_version + job_name + job_version
                  runtime


dagconf

flow_version  -->  branch_name
job_name      -->  file_name
inputs        -->  inputs
outputs       -->  outputs
job_version   -->  job_version
projectId     -->  project_name
timeout       -->  timeout
runtime       -->  python3,R,pyspark,sparkR
