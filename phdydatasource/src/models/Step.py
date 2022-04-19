from marshmallow_jsonapi import fields
from models.Model import Model


class Step(Model):
    type = "steps"
    attributes = {
        "pjName": fields.Str(required=True),
        "stepId": fields.Str(required=True),
        "ctype": fields.Str(dump_default="unknown"),
        "expressions": fields.Str(dump_default="unknown"),
        "groupName": fields.Str(dump_default="unknown"),
        "groupIndex": fields.Int(dump_default=-1),
        "id": fields.Str(dump_default="unknown"),
        "expressionsValue": fields.Str(dump_default="unknown")
    }

