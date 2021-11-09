import pytest
from phemailrepwd.src.main import lambdaHandler


class TestLmd:
    def test_lmd(self):
        data = {"type": "test", "email": "2091038466@qq.com"}
        result = lambdaHandler(data, ' ')
        assert '"test_success"' == result['body']

    def test_lmd1(self):
        data = {"type": "forget_password", "email": "2091038466@qq.com"}
        result = lambdaHandler(data, ' ')
        assert '"repassword success"' == result['body']


if __name__ == '__main__':
    pytest.main()
