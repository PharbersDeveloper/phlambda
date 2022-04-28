from marshmallow_jsonapi import fields
from models.Model import Model


class Execution(Model):
    type = "executions"
    attributes = {
        "smId": fields.Str(required=True),
        "input": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown"),
        "startTime": fields.Int(dump_default=-1),
        "state": fields.Str(dump_default="unknown"),
        "endTime": fields.Int(dump_default=-1),
        "steps": fields.Str()
    }

