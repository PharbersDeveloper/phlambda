from marshmallow_jsonapi import fields
from models.Model import Model


class ScenarioStep(Model):
    type = "scenario-steps"
    attributes = {
        "scenarioId": fields.Str(required=True),
        "index": fields.Int(dump_default=0),
        "detail": fields.Str(dump_default="unknown"),
        "name": fields.Str(dump_default="unknown"),
        "traceId": fields.Str(dump_default="unknown")
    }

