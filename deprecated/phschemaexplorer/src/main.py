import constants.Common as Common
import json
import logging
from constants.Errors import Errors, FileNotFound, NotXlsxFile, NotCsvFile, NotXlsFile
from handler.Reader import Reader


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        result = Reader(body).reader()
        return Common.serialization(result)
    except FileNotFound as e:
        return Common.serialization(e)
    except NotXlsxFile as e:
        return Common.serialization(e)
    except NotCsvFile as e:
        return Common.serialization(e)
    except NotXlsFile as e:
        return Common.serialization(e)
    except Errors as e:
        logging.debug(e)
        return Common.serialization(e)
