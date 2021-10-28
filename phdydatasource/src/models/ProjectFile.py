from marshmallow_jsonapi import fields
from models.Model import Model


class ProjectFile(Model):
    type = "project-files"
    smID = fields.Str()
    name = fields.Str()
    status = fields.Str()
    property = fields.Str()
    date = fields.Int()
    category = fields.Str()
    size = fields.Int()
