from marshmallow_jsonapi import fields
from models.Model import Model


class DataSet(Model):
    type = "versions"
    attributes = {
        "projectId": fields.Str(required=True),
        "datasetId": fields.Str(required=True),
        "name": fields.Str(dump_default="unknown"),
        "date": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown")
    }