from marshmallow_jsonapi import fields
from models.Model import Model


class DagConf(Model):
    type = "dag-confs"
    attributes = {
        "projectId": fields.Str(required=True),
        "jobName": fields.Str(required=True),
        "flowVersion": fields.Str(dump_default="unknown"),
        "dagName": fields.Str(dump_default="unknown"),
        "inputs": fields.Str(dump_default="unknown"),
        "jobDisplayName": fields.Str(dump_default="unknown"),
        "jobId": fields.Str(dump_default="unknown"),
        "jobVersion": fields.Str(dump_default="unknown"),
        "outputs": fields.Str(dump_default="unknown"),
        "owner": fields.Str(dump_default="unknown"),
        "runtime": fields.Str(dump_default="unknown"),
        "targetJobId": fields.Str(dump_default="unknown"),
        "timeout": fields.Str(dump_default="unknown"),
        "labels": fields.Str(dump_default="unknown"),
        "projectName": fields.Str(dump_default="unknown"),
        "jobPath": fields.Str(dump_default="unknown"),
        "jobShowName": fields.Str(dump_default="unknown")
    }

