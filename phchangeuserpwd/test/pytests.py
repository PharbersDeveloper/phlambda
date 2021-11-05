import pytest
from phchangeuserpwd.src.app import Run as run


class TestLmd:
    def test_lmd(self):
        data = {'email': 'pqian@pharbers.com', 'password': '6666666666', 'new_password': '999999'}
        result = run(data)
        print(result)
        assert "password false" == result

    def test_lmd1(self):
        data = {'email': 'pqian@pharbersom', 'password': 'Abcde196125', 'new_password': '999999'}
        result = run(data)
        print(result)
        assert "account false" == result

    def test_lmd2(self):
        data = {'email': 'pqian@pharbers.com', 'password': 'Abcde196125', 'new_password': '999999'}
        result = run(data)
        assert "password len false" == result

    def test_lmd3(self):
        data = {'email': 'pqian@pharbers.com', 'password': 'Abcde196125', 'new_password': '99999ffds9'}
        result = run(data)
        assert "password should format false" == result

    def test_lmd4(self):
        data = {'email': 'pqian@pharbers.com', 'password': 'Abcde196125', 'new_password': 'd经sf!9ffds9'}
        result = run(data)
        assert "password only format false" == result

    def test_lmd5(self):
        data = {'email': 'pqian@pharbers.com', 'password': 'Abcde196125', 'new_password': 'dsf!9ffds9'}
        result = run(data)
        assert "密码更改成功" == result


if __name__ == '__main__':
    pytest.main()


