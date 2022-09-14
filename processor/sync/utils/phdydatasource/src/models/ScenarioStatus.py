from marshmallow_jsonapi import fields
from models.Model import Model


class ScenarioStatus(Model):
    type = "scenario-status"
    attributes = {
        "id": fields.Str(required=True),
        "startAt": fields.Str(dump_default="unknown"),
        "endAt": fields.Str(dump_default="unknown"),
        "status": fields.Str(dump_default="unknown"),
        "name": fields.Str(dump_default="unknown"),
        "scenarioId": fields.Str(dump_default="unknown"),
        "traceId": fields.Str(dump_default="unknown"),
    }

