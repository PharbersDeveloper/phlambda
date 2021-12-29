from handler.Command.Receiver import Receiver
import constants.Common as Common


class LockReceiver(Receiver):

    def __init__(self):
        self.redis = Common.EXTERNAL_SERVICES["redis"].getRedis()

    def lock(self, key, value, time=60):
        if self.redis.setnx(key, value):
            self.redis.expire(key, time)

    def unlock(self, key):
        self.redis.delete(key)

    def watch(self, key):
        return self.redis.exists(key)
