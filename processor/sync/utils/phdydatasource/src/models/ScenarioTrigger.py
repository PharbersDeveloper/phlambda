from marshmallow_jsonapi import fields
from models.Model import Model


class ScenarioTrigger(Model):
    type = "scenario-triggers"
    attributes = {
        "scenarioId": fields.Str(required=True),
        "index": fields.Int(dump_default=0),
        "active": fields.Boolean(dump_default=False),
        "detail": fields.Str(dump_default="unknown"),
        "mode": fields.Str(dump_default="unknown"),
        "resrouceArn": fields.Str(dump_default="unknown"),
        "traceId": fields.Str(dump_default="unknown"),
        "name": fields.Str(dump_default="unknown")
    }

