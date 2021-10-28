from marshmallow_jsonapi import fields
from models.Model import Model


class ProjectFile(Model):
    type = "project-files"
    attributes = {
        "smID": fields.Str(required=True),
        "name": fields.Str(required=True),
        "status": fields.Str(dump_default="unknown"),
        "property": fields.Str(required=True),
        "date": fields.Int(dump_default=-1),
        "category": fields.Str(required=True),
        "size": fields.Int(dump_default=-1)
    }
