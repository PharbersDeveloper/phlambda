from marshmallow_jsonapi import fields
from models.Model import Model


class DataSet(Model):
    type = "datasets"
    attributes = {
        "projectId": fields.Str(required=True),
        "name": fields.Str(required=True),
        "schema": fields.Str(dump_default="unknown"),
        "version": fields.Str(required=True),
        "label": fields.Str(dump_default="unknown"),
        "cat": fields.Str(dump_default="normal"),
        "path": fields.Str(dump_default=""),
        "format": fields.Str(dump_default=""),
        "prop": fields.Str(dump_default=""),
        "date": fields.Int(dump_default=-1),
        "sample": fields.Str(dump_default="F_1")
    }
