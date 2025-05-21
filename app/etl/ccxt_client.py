"""Thin wrapper around ccxt to create rate-limited exchange clients."""

from __future__ import annotations

import importlib


_DEF_OPTIONS = {
    "enableRateLimit": True,
    "timeout": 30_000,
    "options": {"adjustForTimeDifference": True},
}


def get_exchange(name: str):
    """Return an instantiated ccxt exchange.

    Parameters
    ----------
    name:
        Exchange id as used in `ccxt`.

    Returns
    -------
    ccxt.Exchange
        Configured exchange instance.
    """
    ccxt = importlib.import_module("ccxt")
    cls = getattr(ccxt, name)
    exchange = cls(_DEF_OPTIONS)
    return exchange
