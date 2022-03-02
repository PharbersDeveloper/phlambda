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
from handler.Command.RemoveS3Path import RemoveS3Path


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
                    "projectId": item["projectId"],
                    "destination": message["destination"]
                })

                remove_s3_dir = f"""{message.get("provider", "pharbers")}/{item['project_id'].replace('_', '-')}/{message['destination']}"""
                RemoveS3Path().execute({
                    "bucket_name": "ph-platform",
                    "s3_dir": f"""2020-11-11/lake/{remove_s3_dir}"""
                })

                SaveCommand(RemoveDSReceiver()).execute({
                    "message": message,
                    "projectId": item["projectId"]
                })

        except ResourceBusy as e:
            raise e
        except Exception as e:
            raise Errors(e)
        finally:
            if set_key:
                UnLockCommand(LockReceiver()).execute({"key": set_key})
