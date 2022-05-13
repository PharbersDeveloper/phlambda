import math
import random


class GenerateID:
    def __init__(self):
        pass

    @staticmethod
    def generate():
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                  "abcdefghijklmnopqrstuvwxyz" \
                  "0123456789-_"

        charsetLength = len(charset)
        keyLength = 3 * 5

        array = []
        for i in range(keyLength):
            array.append(charset[math.floor(random.random() * charsetLength)])

        return "".join(array)
