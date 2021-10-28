from marshmallow_jsonapi import fields
from models.Model import Model


class Partition(Model):
    type = "partitions"
    smID = fields.Str() # glue table name
    source = fields.Str() # Location
    schema = fields.Str()
    date = fields.Int()
    partitions = fields.Str() # Key - Value
