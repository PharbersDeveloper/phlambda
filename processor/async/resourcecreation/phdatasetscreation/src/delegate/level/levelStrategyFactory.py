

class LevelStrategyFactory(object):
    """策略工厂类"""
    strategy = {}

    @classmethod
    def get_strategy_by_type(cls, level_type):
        """类方法: 根据level_type获取具体的策略类"""
        return cls.strategy.get(level_type)

    @classmethod
    def register(cls, strategy_type, strategy):
        """类方法: 注册策略类型"""
        if strategy_type == "":
            raise Exception("level策略类型为空")
        cls.strategy[strategy_type] = strategy
