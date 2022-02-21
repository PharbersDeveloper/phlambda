import json

from delegate.createDagByItem.command import Command
from delegate.createDagByItem.commandCreateDag import CommandCreateDag
from delegate.createDagByItem.commandCreateDagConf import CommandCreateDagConf
from delegate.createDagByItem.commandUploadAirflow import CommandUploadAirflow
from delegate.createDagByItem.commandPutItemToDB import CommandPutItemToDB
from delegate.createDagByItem.commandCreateDagLevel import CommandCreateDagLevel
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL



def max_script(dag_item):
    logger = PhLogging().phLogger("max_script", LOG_DEBUG_LEVEL)
    logger.debug("dag创建流程")
    message = {
        "status": "",
        "message": ""
    }
    try:
        # 创建dag_conf 返回dag_conf_data
        dag_conf_list = CommandCreateDagConf(dag_item=dag_item).run()
        logger.debug("创建dag_conf成功")
        logger.debug(dag_conf_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_conf时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))

    try:
        # 根据dag_conf_list 创建 Level并返回 dag_item_level_list
        level_type = "SCRIPT_LEVEL"
        dag_item_level_list = CommandCreateDagLevel(dag_conf_list=dag_conf_list, level_type=level_type).run()
        logger.debug("创建dag的level成功")
        logger.debug(dag_item_level_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_level时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))

    try:
        # 创建dag 返回dag_data
        dag_item_list = CommandCreateDag(dag_conf_list=dag_conf_list, dag_item_level_list=dag_item_level_list).run()
        logger.debug("根据level创建dag_item成功")
        logger.debug(dag_item_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_item时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag_item create success"

    try:
        # 将创建好的dag上传到dynamodb
        CommandPutItemToDB(dag_conf_list=dag_conf_list, dag_item_list=dag_item_list).run()
        logger.debug("将创建好的dag_item上传到dynamodb成功")
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "上传dag_item时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag_item upload success"

    try:
        # 创建airflow 返回airflow_data
        CommandUploadAirflow(dag_item=dag_item).run()
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "更新 phjob 运行文件时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag insert success"

    return message


def max_refresh(dag_item):
    logger = PhLogging().phLogger("max_refrash", LOG_DEBUG_LEVEL)
    logger.debug("dag刷新流程")

    message = {
        "status": "",
        "message": ""
    }

    try:
        # 创建dag_conf 返回dag_conf_data
        dag_conf_list = CommandCreateDagConf(dag_item=dag_item).refresh_dagconf()
        logger.debug("创建dag_conf成功")
        logger.debug(dag_conf_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_conf时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))

    try:
        # 根据dag_conf_list 创建 Level并返回 dag_item_level_list
        level_type = "SCRIPT_LEVEL"
        dag_item_level_list = CommandCreateDagLevel(dag_conf_list=dag_conf_list, level_type=level_type).run()
        logger.debug("创建dag的level成功")
        logger.debug(dag_item_level_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_level时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))

    try:
        # 创建dag 返回dag_data
        dag_item_list = CommandCreateDag(dag_conf_list=dag_conf_list, dag_item_level_list=dag_item_level_list).run()
        logger.debug("根据level创建dag_item成功")
        logger.debug(dag_item_list)
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "创建dag_item时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag_item create success"

    try:
        # 将创建好的dag上传到dynamodb
        CommandPutItemToDB(dag_conf_list=dag_conf_list, dag_item_list=dag_item_list).run()
        logger.debug("将创建好的dag_item上传到dynamodb成功")
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "上传dag_item时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag_item upload success"

    try:
        # 创建airflow 返回airflow_data
        CommandUploadAirflow(dag_item=dag_item).run()
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "更新 phjob 运行文件时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag insert success"

    return message


def max_prepare_script(dag_item):
    logger = PhLogging().phLogger("max_prepare_script", LOG_DEBUG_LEVEL)
    logger.debug("prepare脚本修改流程")
    message = {
        "status": "",
        "message": ""
    }
    try:
        # 创建airflow 返回airflow_data
        CommandUploadAirflow(dag_item=dag_item).edit_prepare_phjob(json.loads(dag_item.get("message")))
    except Exception as e:
        message["status"] = "failed"
        message["message"] = "修改prepare脚本时错误:" + json.dumps(str(e), ensure_ascii=False)
        raise Exception(json.dumps(message))
    else:
        message["status"] = "succeed"
        message["message"] = "dag insert success"

    return message
