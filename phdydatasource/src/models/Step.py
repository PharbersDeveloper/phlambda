from marshmallow_jsonapi import fields
from models.Model import Model


class Step(Model):
    type = "steps"
    attributes = {
        "stId": fields.Str(required=True),
        "input": fields.Str(),
        "output": fields.Str(),
        "startTime": fields.Int(),
        "state": fields.Str(),
        "endTime": fields.Int(),
        "stepLog": fields.Str(),
        "logLocation": fields.Str()
    }

