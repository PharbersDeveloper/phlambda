from marshmallow_jsonapi import Schema, fields


class Convert2JsonAPI:

    def __init__(self, model, many=False):
        self.model = model

        class BuildClass(Schema):
            id = fields.Str(dump_only=True)

            class Meta:
                type_ = model.type

        self.mc = BuildClass(many=many)
        for filed in self.model.attributes.keys():
            self.mc.dump_fields[filed] = self.model.attributes[filed]
            self.mc.fields[filed] = self.model.attributes[filed]

    def build(self):
        return self.mc
