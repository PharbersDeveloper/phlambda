from marshmallow_jsonapi import fields
from models.Model import Model


class DataSet(Model):
    type = "datasets"
    attributes = {
        "projectID": fields.Str(required=True),
        "name": fields.Str(required=True),
        "schema": fields.Str(dump_default="unknown"),
        "version": fields.Str(required=True),
        "label": fields.Str(dump_default="unknown")
    }
