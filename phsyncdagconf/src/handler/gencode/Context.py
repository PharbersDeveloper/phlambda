from handler.gencode.Strategy import Strategy


class Context:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def do_execution(self, data):
        return self._strategy.do_execution(data)
