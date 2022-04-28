from marshmallow_jsonapi import fields
from models.Model import Model


class Notification(Model):
    type = "notifications"
    attributes = {
        "projectId": fields.Str(required=True),
        "owner": fields.Str(dump_default="unknown"),
        "showName": fields.Str(dump_default="unknown"),
        "code": fields.Str(dump_default="unknown"),
        "jobDesc": fields.Str(dump_default="unknown"),
        "jobCat": fields.Str(dump_default="unknown"),
        "comments": fields.Str(dump_default="unknown"),
        "message": fields.Str(dump_default="{}"),
        "date": fields.Int(dump_default=-1)
    }

