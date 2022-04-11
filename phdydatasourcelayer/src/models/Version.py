from marshmallow_jsonapi import fields
from models.Model import Model


class Version(Model):
    type = "version"
    attributes = {
        "project_id": fields.Str(required=True),
        "sort_key": fields.Str(required=True),
        "name": fields.Str(dump_default=""),
        "owner": fields.Str(dump_default=""),
        "updatetime": fields.Int(dump_default=0),
        "version_msg": fields.Str(dump_default=""),
    }
