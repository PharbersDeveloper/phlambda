from util.NotificationType.Strategy import Strategy


class Context:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def run(self, data):
        return self._strategy.do_exec(data)
