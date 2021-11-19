import os
import pytest
import json
import src.app as app

os.environ["PATH_PREFIX"] = "/Users/qianpeng/Desktop/"
os.environ["BATCH_SIZE"] = "200"
os.environ["CLICKHOUSE_HOST"] = "localhost"
os.environ["CLICKHOUSE_PORT"] = "19000"
os.environ["CLICKHOUSE_DB"] = "default"
os.environ["AWS_ACCESS_KEY_ID"] = "ASIAWPBDTVEAKQBHFKOA"
os.environ["AWS_SECRET_ACCESS_KEY"] = "3ZIeG4JqkuwS6TdRazidgSRjnmP8xYRqi39lBJBH"
os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEAgaDmNuLW5vcnRod2VzdC0xIkgwRgIhAPVZ558iUkV3Cs4WOhWDjdi1riiJGxZuF2XGbb9P3SnVAiEAnPC7/ysdiLwba+7tuF4iG+YaPeakV5qAF4UNDYA8k+8qlwIINhACGgw0NDQ2MDM4MDM5MDQiDA/luBim5qy2loEJVSr0AY7uZ2YLX02sFb9XIKYLIbFB6/cnDJV6MK9mfB6r9pzukHaZ9jrdZqBgFC6qZLUxfy5rW5Q0E0A5Fihnvn3L7bbjnoJXLWwzjoqoaiBQ0Hxx6Lk9X+oXw1lXS1C4ilorTOjEXqtICYz05l5ZWVjNwmsYptCl6t2Sbca/DEQrgE3tS+STEKfsT1QzO4b3+4U6s5QHUh0XNxCHK9OPDqTAqlbHQ5IDj9h9MCbBG/7Z12lQ/uTJuxU0hLkBMaAA16wFVVo/8tQv2Df1Otpfmnb83rYw3bpEVU+6pHoX5jsPuBYKoCqi29bpSU85GWXoJJfzvwhiWKYwqaTZjAY6nAGiz9gDC2slXuNokS4fWL3pQ74lThi5lvKV/qnjZPuMSQD6HhI2l/9MKFAgSna8461QyT5/oUByNGNcqEHsaSaOg0pYh7JDT3XpsbbrF9D7mwmvWEC/5zzbP3v+CP9oAk2OjfxxCCnlAL91wNzvA9IQ+oHsw5ZVoxAeMeCcsxcSh5jv7bb64yUes4rwz3IraQgSrlbz9Dyk39fmtJc="


class TestLmd:
    def test_lmd(self):
        event = open("../events/event.json", "r").read()
        result = app.lambda_handler(json.loads(event), None)
        print(result)
        # assert 'e' in a


if __name__ == '__main__':
    pytest.main()
