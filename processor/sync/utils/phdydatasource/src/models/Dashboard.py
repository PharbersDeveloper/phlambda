from marshmallow_jsonapi import fields
from models.Model import Model


class Dashboard(Model):
    type = "dashboards"
    attributes = {
        "projectId": fields.Str(required=True),
        "dashboardId": fields.Str(required=True),
        "description": fields.Str(dump_default="unknown"),
        "title": fields.Str(dump_default="unknown"),
        "updating": fields.Int(dump_default="unknown"),
        "label": fields.Str(dump_default="unknown")
    }
