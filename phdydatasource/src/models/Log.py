from marshmallow_jsonapi import fields
from models.Model import Model


class Log(Model):
    type = "logs"
    attributes = {
        "runId": fields.Str(required=True),
        "jobId": fields.Str(required=True),
        "airflowRunId": fields.Str(dump_default="unknown"),
        "emrLog": fields.Str(dump_default="unknown"),
        "lmdLog": fields.Str(dump_default="unknown"),
        "localLog": fields.Str(dump_default="unknown"),
        "logType": fields.Str(dump_default="unknown"),
        "sfnLog": fields.Str(dump_default="unknown")
    }

