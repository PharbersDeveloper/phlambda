import os
import boto3
import random

def upload_code(zip_name, project_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(
        Bucket="ph-platform",
        Key="2020-11-11/cicd/"+ project_name +"/source/code.zip",
        Filename="/tmp/" + project_name + "/" + zip_name
    )


def start_codebuild():
    client = boto3.client('codebuild')

    response = client.list_projects(
        sortOrder='ASCENDING'
    )
    codebuild_project = [
        "codebuild-manager-phtmppsycopg-12PJ2Z17IMXBJ",
        "codebuild-manager-phdagrunid-GISP8T92O80H",
        "codebuild-manager-phschemaexplorer-1KIBP193HKMD8",
        "codebuild-manager-phcreatestepargs-1RGW6KBWOR4H4",
        "codebuild-manager-phapplyuser-13JOYOH6XC9Z2",
        "codebuild-manager-phemberedviews-VMN3MZNM5J5Q",
        "codebuild-manager-phs3explorer-HE94WK61V5YL",
        "codebuild-manager-phtm-10DGASKZWQXLQ",
        "codebuild-manager-phjsonapi-QXELLIO9HMRM",
        "codebuild-manager-phrollback-5BA01BBMUW47",
        "codebuild-manager-phclickhousesql-T2WHY3VMGFQX",
        "codebuild-manager-phauthentication-Z3YDFXW8VEUW",
        "codebuild-manager-phchupdatesql-GP33T7R3ZY2A",
        "codebuild-manager-phchdatasource-1K69LQYASIRS6",
        "codebuild-manager-phxlsxtockhouse-A338SLQXVFO6",
        "codebuild-manager-phpowerbi-183I3RBZ9OZ23",
        "codebuild-manager-phoffweb-1AAVN6GTL925T",
        "codebuild-manager-phetlstepargs-X18HDXYNPRJ8",
        "codebuild-manager-phetlsfn-TQZQ34PKB5K6",
        "codebuild-manager-phnoticeglue-1LMGBANNINAEF",
        "codebuild-manager-phgetsfn-NOEYAZ5JRMF2",
        "codebuild-manager-phreport-Q4MG0DGMDK7Q",
        "codebuild-manager-phnoticeemail-V77NNXP745NE",
        "codebuild-manager-phstartcrawler-MV0BLYXOJ14P",
        "codebuild-manager-phcicd-646HTSFSVSV9",
        "codebuild-manager-phaccounts-1EECDPT63XCA7",
        "codebuild-manager-phcatlog-1DON0FZEHDD98",
        "codebuild-manager-phmax-1IHQYCDB68QKE",
        "codebuild-manager-phgluejob-LZ0PHHCPTX66",
        "codebuild-manager-phstepfunctionindex-1UP6U77WVUA7Z",
        "codebuild-manager-phnoticesms-10SXZ8JKPD9GB",
        "codebuild-manager-phnoticeiot-7MBX1WD8N759",
        "codebuild-manager-phworkflow-WQ1200XL11W5",
        "codebuild-manager-phcommon-VE1YB7TUCPJW",
        "codebuild-manager-phuseragent-5I8QRJOVNZD1",
        "codebuild-manager-phoauth-1AYB08O06FG1E",
        "codebuild-manager-phproject-52I197EZAXJI",
        "codebuild-manager-phentry-15JV3GXDNS206",
        "codebuild-manager-phglueindex-13NB41DGVPNKI",
    ]
    for project in response['projects']:
        client.start_build(
            projectName=project,
        )


def update_version(git_commit_version):
    # 修改README文件 填写版本号
    create_readme_file_cmd = "sed -i s/{git_commit_version}/" + git_commit_version + "/ src/README.md"
    os.system(create_readme_file_cmd)


def zip_code(local_path, git_event):
    git_commit_version = git_event["git_commit_version"]
    lmd_project_names = ["phaccounts",
                   "phapplyuser",
                   "phauthentication",
                   "phcatlog",
                   "phchdatasource",
                   "phchupdatesql",
                   "phcicd",
                   "phclickhousesql",
                   "phcommon",
                   "phcreatestepargs",
                   "phdagrunid",
                   "phemberedviews",
                   "phentry",
                   "phetlsfn",
                   "phetlstepargs",
                   "phgetsfn",
                   "phglueindex",
                   "phgluejob",
                   "phjsonapi",
                   "phmax",
                   "phnoticeemail",
                   "phnoticeglue",
                   "phnoticeiot",
                   "phnoticesms",
                   "phoauth",
                   "phoffweb",
                   "phpowerbi",
                   "phproject",
                   "phreport",
                   "phrollback",
                   "phs3explorer",
                   "phschemaexplorer",
                   "phstartcrawler",
                   "phstepfunctionindex",
                   "phtm",
                   "phtmppsycopg",
                   "phuseragent",
                   "phworkflow",
                   "phxlsxtockhouse"
                   ]
    for project_name in os.listdir(local_path):
        if project_name in lmd_project_names:
            code_path = local_path + "/" + project_name + "/"
            if os.path.isdir(code_path):
                # 创建文件夹
                mkdir_cmd = "mkdir /tmp/" + project_name
                os.system(mkdir_cmd)

                # 复制ph_get_execution_status下的代码到当前目录下
                key_str = ""
                for key in os.listdir(code_path):
                    if os.path.isdir(code_path + key):
                        cp_cmd = "cp -r " + code_path + key + "/" + " /tmp/" + project_name + "/"
                    else:
                        cp_cmd = "cp -r " + code_path + key + " /tmp/" + project_name + "/"
                    os.popen(cp_cmd)
                    key_str = key_str + key + " "
                os.chdir("/tmp/" + project_name)

                # 修改README文件 修改git_commit_version
                update_version(git_commit_version)

                # 打包代码为code.zip
                zip_name = "code.zip"
                zip_cmd = "zip -r " + zip_name + " " + key_str
                os.system(zip_cmd)

                # 上传code到s3
                upload_code(zip_name, project_name)

if __name__ == '__main__':
    local_path = "/home/hbzhao/PycharmProjects/pythonProject/phlambda"
    git_commit_version = "6814732cc39"
    zip_code(local_path, git_commit_version)