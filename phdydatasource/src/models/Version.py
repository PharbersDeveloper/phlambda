from marshmallow_jsonapi import fields
from models.Model import Model


class Version(Model):
    type = "versions"
    attributes = {
        "projectId": fields.Str(required=True),
        "datasetId": fields.Str(required=True),
        "name": fields.Str(required=True),
        "date": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown")
    }
