from marshmallow_jsonapi import fields
from models.Model import Model


class Execution(Model):
    type = "executions"
    smId = fields.Str()
    input = fields.Str()
    owner = fields.Str()
    startTime = fields.Int()
    state = fields.Str()
    endTime = fields.Int()
    steps = fields.Str()
