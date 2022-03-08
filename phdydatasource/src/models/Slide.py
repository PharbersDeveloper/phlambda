from marshmallow_jsonapi import fields
from models.Model import Model


class Slide(Model):
    type = "slides"
    attributes = {
        "id": fields.Str(required=True),
        "pdId": fields.Str(required=True),
        "slideId": fields.Str(required=True),
        "idx": fields.Int(dump_default=0),
        "title": fields.Str(dump_default="unknown"),
        "content": fields.Str(dump_default="unknown")
    }
