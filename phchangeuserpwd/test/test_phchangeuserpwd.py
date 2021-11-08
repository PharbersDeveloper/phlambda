import pytest
from phchangeuserpwd.src.main import lambdaHandler


class TestLmd:
    def test_lmd(self):
        data = {
            "body": "{\"id\": \"qtaGDePl1OrSFEgm\",\"password\": \"4c4cc360324690e719a628c83287201cb0a2e0e512b53c33d7135c7ba9dda9d6\",\"new_password\": \"1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582\"}", }
        result = lambdaHandler(data, ' ')
        assert '"repassword False"' == result['body']
    def test_lmd1(self):
        data = {
            "body": "{\"id\": \"qtaGDePl1OrSFEgm\",\"password\": \"1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582\",\"new_password\": \"4c4cc360324690e719a628c83287201cb0a2e0e512b53c33d7135c7ba9dda9d6\"}", }
        result = lambdaHandler(data, ' ')
        assert '"repassword success"' == result['body']

if __name__ == '__main__':
    pytest.main()
