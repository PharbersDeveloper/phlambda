import pandas as pd
from functools import reduce
from handler.Command.Receiver import Receiver
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class WriteReceiver(Receiver):

    def __init__(self):
        self.logger = PhLogging().phLogger("Write Parquet", LOG_DEBUG_LEVEL)

    def write(self, data):
        self.logger.debug("Parquet")
        write_path = data["writePath"]
        execl_data = data["execlData"]
        schema = list(execl_data[0].keys())
        df_data = reduce(lambda pre, next: dict(pre, **next),
                      list(map(lambda key: {key: list(map(lambda x: x[key], execl_data))}, schema)))

        df = pd.DataFrame(data=df_data)
        df.to_parquet(write_path, index=False, partition_cols="version")



