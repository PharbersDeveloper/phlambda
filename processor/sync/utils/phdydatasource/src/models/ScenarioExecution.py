from marshmallow_jsonapi import fields
from models.Model import Model


class ScenarioExecution(Model):
    type = "scenario-executions"
    attributes = {
        "scenarioId": fields.Str(required=True),
        "runnerId": fields.Str(dump_default="unknown"),
        "date": fields.Int(dump_default=0),
        "owner": fields.Str(dump_default="unknown"),
        "reporter": fields.Str(dump_default="unknown"),
        "runtime": fields.Str(dump_default="unknown")
    }

