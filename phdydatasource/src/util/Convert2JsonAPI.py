from marshmallow_jsonapi import Schema, fields


class Convert2JsonAPI:

    def __init__(self, model):
        class BuildClass(Schema, model):
            id = fields.Str(dump_only=True)

            class Meta:
                type_ = model.type

        self.mc = BuildClass

    def build(self):
        return self.mc()
