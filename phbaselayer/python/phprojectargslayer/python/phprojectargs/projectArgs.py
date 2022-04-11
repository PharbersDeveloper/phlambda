from phprojectargs.utils.AWS.SSM import SSM
from phprojectargs.utils.Errors import ResourceNotCreateError


class ProjectArgs(object):

    def __init__(self, project_id):
        self.ssm = SSM()
        self.project_id = project_id
        self.__args = self.__get_args_from_ssm()

    def __get_args_from_ssm(self):
        args = self.ssm.get_dict_ssm_parameter(self.project_id)
        if args == "参数不存在":
            raise ResourceNotCreateError("资源未启动")
        return args

    def get_parameter(self, parameter_key):
        return self.__args.get(parameter_key)

    def get_project_name(self):
        return self.__args.get("projectName")

    def get_project_dns(self):
        return self.__args.get("dns")

    def get_current_context(self):
        return self.__args.get("currentContext")

    def get_proxy_list(self):
        return self.__args.get("proxies")

    def get_cluster_list(self):
        return self.__args.get("clusters")

    def get_olap_list(self):
        return self.__args.get("olap")

    def get_action_id(self):
        return self.__args.get("notification")

    def get_common_args(self):
        return self.__args.get("commargs")
