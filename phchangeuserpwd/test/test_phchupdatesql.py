import pytest
import sys
sys.path.insert(0, '../..')
from phchangeuserpwd.src.main import Run



class TestLmd:
    def test_lmd(self):
        data = {'id': 'fdasfds',
                'password': '1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582',
                'new_password': '4c4cc360324690e719a628c83287201cb0a2e0e512b53c33d7135c7ba9dda9d6'}
        result = Run(data, ' ')
        assert "账户不正确" == result

    def test_lmd1(self):
        data = {'id': 'qtaGDePl1OrSFEgm',
                'password': '1cd7fc9d631b3541ae5f668e02e7c9472d9f0f56f83ccf2bc582',
                'new_password': '4c4cc360324690e719a628c83287201cb0a2e0e512b53c33d7135c7ba9dda9d6'}
        result = Run(data, ' ')
        assert "密码不正确" == result

    def test_lmd2(self):
        data = {'id': 'qtaGDePl1OrSFEgm',
                'password': '1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582',
                'new_password': '4c4cc360324690e719a628c83287201cb0a2e0e512b53c33d7135c7ba9dda9d6'}
        result = Run(data, ' ')
        assert "密码修改成功" == result


if __name__ == '__main__':
    pytest.main()

