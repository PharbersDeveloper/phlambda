import os

def upload_code():
    pass

def package_code():

    local_path_prefix = '/home/hbzhao/PycharmProjects/pythonProject/phlambda/phcicd/parse_event/src'
    local_path = os.path.join(local_path_prefix, 'phlambda')
    code_path = local_path + "/phworkflow/ph_get_execution_status/"
    # 复制ph_get_execution_status下的代码到当前目录下
    key_str = ""
    for key in os.listdir(code_path):
        print(code_path + key)
        cp_cmd = "cp -r " + code_path + key + " " + local_path_prefix
        os.popen(cp_cmd)
        key_str = key_str + key + " "
    # 打包代码为code.zip
    zip_cmd = "zip -r -q " + local_path_prefix + "/code.zip " + key_str
    os.popen(zip_cmd)
    print(zip_cmd)

    # 删除复制来的代码


if __name__ == '__main__':
    package_code()