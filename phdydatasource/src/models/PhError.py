from marshmallow_jsonapi.exceptions import JSONAPIError


class PhError(JSONAPIError):
    pointer = "/data/type"
    default_message = 'Invalid type. Expected "{expected}".'
    code = 0

    def __init__(self, message=None, pointer=None):
        self.detail = message or self.default_message
        self.pointer = pointer or self.pointer
        super().__init__(self.detail)

    @property
    def messages(self):
        return {
            "errors": [{"detail": self.detail, "source": {"pointer": self.pointer}}]
        }
