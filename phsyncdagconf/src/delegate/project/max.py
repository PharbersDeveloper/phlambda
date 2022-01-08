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


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )

@singleton
class Max(Project):

    def __init__(self, **kwargs):
        self.updateAction = UpdateAction()
        pass
        # for key, val in kwargs.items():
        #     setattr(self, key, val)

        # TODO: 这个地方用Facade合适吗？不要靠本能写程序！！！！！
        # 在设计上，需要对以下五个地方进行重构：
        # 1. 不同的project 创建不同的实体，这是典型的工厂，工厂本身是单例，类实例之间的管理还是用单例
        # 2. 同时，创建的流程是一个状态机，每一步的状态机都是一个Command命令设计模式
        #       利用这样的流程可以去掉所有的if与switch，这就是继承和多态的正确用法
        #   2.1 在状态机器上，加入异常的抓取，对每一步的异常形成具体的错误类，对每一个类确定固定的返回值
        #       这种设计模式叫Null Object的变体
        # 3. 最后，如果没有任何异常后，在统一更新数据库，这样你在中间数据出现任何的错误都不会对存储数据产生影响
        #       在没有回滚机制的NoSQL数据库中不能依赖SQL的batch Update机制
        #       也就是需要在编程思想上解决对SQL的依赖，特别是回滚,
        #       同时还需要保证在数据创建失败的情况下，不影响Airflow的原先的dag文件
        # 4. 对这个函数加入一个分布式锁，利用projectId作为自己的钥匙，写到Redis中，保证一次在同一个项目中只能有一个人
        #       能创建job
        # 5. 利用策略模式，把创建所有level的流程，抽离出来，这个部分会长期修改，并可能不由你单人修改


    def exec(self, dag_item, dag_type):

        logging.info("开始对dag进行操作")
        logging.info(dag_type)

        # , "createDag", "createAirflowFile"
        max_job_cats = {
            "dag_refresh": maxRefrash,
            "prepare_edit": maxPrepareScript,
            "dag_create": maxCreate
        }

        # 创建redis连接
        redis_lock = dag_item.get("projcetId") + "_" + dag_item.get("jobCat")
        redis_cli = create_redis_lock()

        if redis_cli.setnx(redis_lock, time.time()):
            redis_cli.expire(redis_lock, 60)
            try:
                status = max_job_cats.get(dag_type)(dag_item)
            except Exception as e:
                status = json.dumps(str(e), ensure_ascii=False)
            finally:
                self.updateAction.updateNotification(dag_item, "notification", dag_conf={}, status=status)
                logging.info("更新notification状态成功")
                logging.info(status)
        redis_cli.delete(redis_lock)
