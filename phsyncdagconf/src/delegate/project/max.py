import logging
import json
import time

from delegate.singleton import singleton
from delegate.project.initproject import Project
from delegate.createDagByItem.commandExecute import max_script as maxCreate
from delegate.createDagByItem.commandExecute import max_refrash as maxRefrash
from delegate.createDagByItem.commandExecute import max_prepare_script as maxPrepareScript
from delegate.lock.redisLock import create_redis_lock
from delegate.updateAction import UpdateAction
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL

@singleton
class Max(Project):

    def __init__(self, **kwargs):
        self.updateAction = UpdateAction()
        self.logger = PhLogging().phLogger("max_project", LOG_DEBUG_LEVEL)

    def exec(self, dag_item, dag_type):

        self.logger.debug("开始对dag进行操作")
        self.logger.debug(dag_type)

        # , "createDag", "createAirflowFile"
        max_job_cats = {
            "dag_refresh": maxRefrash,
            "prepare_edit": maxPrepareScript,
            "dag_create": maxCreate
        }

        # # 创建redis连接
        # redis_lock = dag_item.get("projcetId") + "_" + dag_item.get("jobCat")
        # redis_cli = create_redis_lock()
        #
        # if redis_cli.setnx(redis_lock, time.time()):
        #     redis_cli.expire(redis_lock, 60)
        try:
            status = max_job_cats.get(dag_type)(dag_item)
        except Exception as e:
            status = json.dumps(str(e), ensure_ascii=False)
        finally:
            self.updateAction.updateNotification(dag_item, "notification", dag_conf={}, status=status)
            self.logger.debug("更新notification状态成功")
            self.logger.debug(status)
        # redis_cli.delete(redis_lock)
