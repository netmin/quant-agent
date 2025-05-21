import sys
from types import ModuleType

# ruff: noqa: E402

import pytest


# create a fake ccxt module with one exchange class
class FakeExchange:
    def __init__(self, opts):
        self.options = opts

    def ping(self):
        return 'pong'


class FakeCCXT(ModuleType):
    binance = FakeExchange


sys.modules['ccxt'] = FakeCCXT('ccxt')

from app.etl.ccxt_client import get_exchange


def test_get_exchange_returns_instance():
    ex = get_exchange('binance')
    assert isinstance(ex, FakeExchange)
    assert ex.options['timeout'] == 30_000


def test_get_exchange_unknown_raises():
    with pytest.raises(AttributeError):
        get_exchange('nosuch')
