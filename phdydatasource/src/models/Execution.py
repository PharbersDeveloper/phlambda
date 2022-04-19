from marshmallow_jsonapi import fields
from models.Model import Model


class Execution(Model):
    type = "executions"
    attributes = {
        "projectId": fields.Str(required=True),
        "jobIndex": fields.Str(required=True),
        "status": fields.Str(dump_default="unknown"),
        "jobName": fields.Str(dump_default="unknown"),
        "desc": fields.Str(dump_default="unknown"),
        "logs": fields.Str(dump_default="unknown"),
        "jobShowName": fields.Str(dump_default="unknown"),
        "startAt": fields.Str(dump_default="unknown"),
        "endAt": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown"),
        "runnerId": fields.Str(dump_default="unknown"),
        "id": fields.Str(dump_default="unknown"),
        "executionTemplate": fields.Str(dump_default="unknown")
    }

