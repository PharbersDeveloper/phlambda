from marshmallow_jsonapi import fields
from models.Model import Model


class Resource(Model):
    type = "resources"
    attributes = {
        "tenantId": fields.Str(required=True),
        "id": fields.Str(required=True),
        "owner": fields.Str(required=False),
        "ownership": fields.Str(required=False),
        "platform": fields.Str(required=False),
        "properties": fields.Str(required=False),
        "resultPath": fields.Str(required=False),
        "role": fields.Str(required=False),
        "ctype": fields.Str(required=False),
        "label": fields.Str(required=False),
        "name": fields.Str(required=False),
        "priority": fields.Int(dump_default=0)
    }
