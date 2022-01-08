import json

from delegate.createDagByItem.command import Command
from util.AWS.DynamoDB import DynamoDB
from delegate.level.scriptLevel import ScriptLevel
from delegate.level.levelStrategyFactory import LevelStrategyFactory
from util.AWS import define_value as dv
from delegate.updateAction import UpdateAction
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class CommandCreateDagLevel(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def InitialStrategys(self):
        """初始化方法: 策略函数"""
        ScriptLevel().collect_context()

    def run(self):
        self.InitialStrategys()
        strategy = LevelStrategyFactory.get_strategy_by_type(self.level_type)
        if not strategy:
            raise Exception("输入的level策略不正确")
        return strategy().create_level(self.dag_conf_list)


