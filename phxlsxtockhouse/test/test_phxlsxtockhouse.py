import os
import pytest
import json
import src.app as app

os.environ["PATH_PREFIX"] = "/Users/qianpeng/Desktop/"
os.environ["BATCH_SIZE"] = "200"
os.environ["CLICKHOUSE_HOST"] = "localhost"
os.environ["CLICKHOUSE_PORT"] = "19000"
os.environ["CLICKHOUSE_DB"] = "default"
os.environ["AWS_ACCESS_KEY_ID"] = "ASIAWPBDTVEAM4MNPL7U"
os.environ["AWS_SECRET_ACCESS_KEY"] = "i+R8WWXWsoHDn1YEUMnSbnqqlxk0UjDJ4x/oklFu"
os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEDcaDmNuLW5vcnRod2VzdC0xIkgwRgIhAMfqlq77xlPEBTScGAFn7CjJ0VsVzJyP6xO8Kxr6MzHjAiEA1nC8J+w0jMitewA8OCoC2jZGWLYvy0OEVOZ1ny0ieicqlwIIZBACGgw0NDQ2MDM4MDM5MDQiDNVtvg5v0LpYpKpApyr0AWL2kqjUSInLbiHcYG708OklUC3mXDairX767LhCrJSQYXR/TxHyd/LHXL8XImUze0cYscEpfey/7DwqrNJ1wJ1hd/YQXLsjtgdZmSRO1R7PwAQk81z0l4h4hkn+Xa9jv1pBL1b8/MkJZxF1zhzZrPskIrlW0xbg5xBt4yYuMc9qg5EswmoMvjzsNQ8Sd6oMEaXb0Hiz0mOR3QdHIzbqiCLCp3hdn3G4P/n+AxTuONolXg0no5zugkpBAwDz5iT7Ey0/Ud8jW74LXrwzRIVBL4kt4EQyf1NBzK1BsGTetuF+kGsV+mdYtL1wobpr8xM89nFbahIwrsnjjAY6nAHvRfByPqp/OmOmMn1KrqWiN+83vUiLof7fCJv2+TbNNQqfDI5Ds9awFTnmuNRfFk82vvfO2fXBC8V+d7qzV8dq2qbH8v4AaMbw0e3E6QdKX1J1s5RyXoQWAxWht7ngV7gQZ2VqZW/CgIRDPpvUALWepe6SKCVeO8oyqAX981ZceQ9axFJ+2e/7QMBg0jfX1XOr7Gjp6tvchEedcKY="


class TestLmd:
    def test_lmd(self):
        event = open("../events/event.json", "r").read()
        result = app.lambda_handler(json.loads(event), None)
        print(result)
        # assert 'e' in a


if __name__ == '__main__':
    pytest.main()
