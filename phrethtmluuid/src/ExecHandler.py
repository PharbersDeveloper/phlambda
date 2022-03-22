import re
import json
from marshmallow_jsonapi import Schema, fields


class Convert2JsonAPI:

    def __init__(self, model, many=False):
        self.model = model

        def dasherize(text):
            return re.sub(r'([a-z])([A-Z])', r'\1-\2', text).lower()

        class BuildClass(Schema):
            id = fields.Str(dump_only=True)

            class Meta:
                type_ = model.type
                inflect = dasherize

        self.mc = BuildClass(many=many)
        for filed in self.model.attributes.keys():
            self.mc.dump_fields[filed] = self.model.attributes[filed]
            self.mc.fields[filed] = self.model.attributes[filed]

    def build(self):
        return self.mc


class Model:
    def __init__(self, kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class Html(Model):
    type = "Html"
    attributes = {
        "uuid": fields.Str(required=True),
        "data": fields.Str(dump_default="unknown"),
    }


__table_structure = {
    "html": Html,
}


def html(data):
    # data = {'uuid': '虎年大吉福享新春，Pharbers邀请您来抢虎年鸿运红包', "titile": "abcde",}
    result = __table_structure["html"](data)
    json_api_data = json.loads(Convert2JsonAPI(__table_structure["html"], many=False).build().dumps(result))
    return json_api_data
