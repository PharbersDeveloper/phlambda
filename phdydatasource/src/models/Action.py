from marshmallow_jsonapi import fields
from models.Model import Model


class Action(Model):
    type = "actions"
    projectId = fields.Str()
    owner = fields.Str()
    showName = fields.Str()
    time = fields.Int()
    code = fields.Str()
    jobDesc = fields.Str()
    jobCat = fields.Str()
    comments = fields.Str()
    message = fields.Str()
    date = fields.Int()
