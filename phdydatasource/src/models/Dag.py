from marshmallow_jsonapi import fields
from models.Model import Model


class Dag(Model):
    type = "dags"
    attributes = {
        "projectId": fields.Str(required=True),
        "sortVersion": fields.Str(dump_default="unknown"),
        "cat": fields.Str(dump_default="unknown"),
        "cmessage": fields.Str(dump_default="unknown"),
        "ctype": fields.Str(dump_default="unknown"),
        "flowVersion": fields.Str(dump_default="unknown"),
        "level": fields.Str(dump_default="unknown"),
        "name": fields.Str(dump_default="unknown"),
        "position": fields.Str(dump_default="unknown"),
        "representId": fields.Str(dump_default="unknown")
    }

