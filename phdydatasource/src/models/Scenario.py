from marshmallow_jsonapi import fields
from models.Model import Model


class Scenario(Model):
    type = "scenarios"
    attributes = {
        "projectId": fields.Str(required=True),
        "scenarioName": fields.Str(dump_default="unknown"),
        "index": fields.Int(dump_default=-1),
        "active": fields.Boolean(dump_default=False),
        "args": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown"),
        "traceId": fields.Str(dump_default="unknown"),
        "label": fields.Str(dump_default="unknown")
    }

