class Receiver:
    def __init__(self):
        pass

    def execute(self, path):
        with open(path, "r") as file:
            return file.read()
