import os
import time
import constants.Common as Common
import constants.DefinValue as DV
from constants.Errors import Errors, ResourceBusy
from handler.Command.SaveCommand import SaveCommand
from handler.Command.LockCommand import LockCommand, UnLockCommand, WatchLockCommand
from handler.Command.RemoveCKReceiver import RemoveCKReceiver
from handler.Command.RemoveDSReceiver import RemoveDSReceiver
from handler.Command.LockReceiver import LockReceiver


class RemoveDS:
    def __init__(self):
        self.redis = Common.EXTERNAL_SERVICES["redis"].getRedis()

    def exec(self, item):
        set_key = None
        try:
            for message in item["message"]:
                check_key = f"""{os.environ[DV.CHECK_APP_NAME]}_{item["projectId"]}_{message["destination"]}"""
                set_key = f"""{os.environ[DV.LOCK_APP_NAME]}_{item["projectId"]}_{message["destination"]}"""
                WatchLockCommand(LockReceiver()).execute({"key": check_key})
                LockCommand(LockReceiver()).execute({
                    "key": set_key,
                    "value": int(round(time.time() * 1000)),
                    "time": 60
                })
                SaveCommand(RemoveCKReceiver()).execute({
                    "tableName": f"""{item["projectId"]}_{message["destination"]}"""
                })

                SaveCommand(RemoveDSReceiver()).execute(item)
                # if self.redis.exists(check_key):
                #     raise ResourceBusy("Resources Are Busy")
                # else:
                #     if self.redis.setnx(set_key, int(round(time.time() * 1000))):
                #         self.redis.expire(set_key, 60)
                #
                #     SaveCommand(RemoveCKReceiver()).execute({
                #         "tableName": f"""{item["projectId"]}_{message["destination"]}"""
                #     })
                #
                #     SaveCommand(RemoveDSReceiver()).execute(item)
                #
                #     # self.removeClickHouseData(item["projectId"] + "_" + message["destination"])
                #     # self.removeDynamoDBData("dataset", message["dsid"], item["projectId"])
                #     self.redis.delete(set_key)
        except ResourceBusy as e:
            raise e
        except Exception as e:
            raise Errors(e)
        finally:
            if set_key:
                UnLockCommand(LockReceiver()).execute({"key": set_key})
