from marshmallow_jsonapi import fields
from models.Model import Model


class ExecutionStatus(Model):
    type = "execution-status"
    attributes = {
        "projectId": fields.Str(required=True),
        "runnerId": fields.Str(dump_default="unknown"),
        "date": fields.Str(dump_default="unknown"),
        "current": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown"),
        "status": fields.Str(dump_default="unknown"),
    }
