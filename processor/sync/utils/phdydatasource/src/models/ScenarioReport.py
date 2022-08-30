from marshmallow_jsonapi import fields
from models.Model import Model


class ScenarioReport(Model):
    type = "scenario-reports"
    attributes = {
        "scenarioId": fields.Str(required=True),
        "index": fields.Int(dump_default=0),
        "detail": fields.Str(dump_default="unknown"),
        "mode": fields.Str(dump_default="unknown"),
        "name": fields.Str(dump_default="unknown"),
        "active": fields.Boolean(dump_default=False),
        "traceId": fields.Str(dump_default="unknown")
    }

