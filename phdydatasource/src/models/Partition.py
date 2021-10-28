from marshmallow_jsonapi import fields
from models.Model import Model


class Partition(Model):
    type = "partitions"
    attributes = {
        "smID": fields.Str(required=True),  # glue table name
        "source": fields.Str(dump_default="unknown"),  # Location
        "schema": fields.Str(dump_default="unknown"),
        "date": fields.Int(dump_default=-1),
        "partitions": fields.Str(dump_default="unknown")  # Key - Value
    }

