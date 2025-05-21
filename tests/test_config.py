from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError
import pytest


# ---------- Pydantic models ----------


class SandboxCfg(BaseModel):
    cpu_limit: int = Field(gt=0, le=8)
    memory_limit_mb: int = Field(ge=256)
    disk_limit_mb: int = Field(ge=50)
    network: bool


class MetricsCfg(BaseModel):
    sharpe_min: float = Field(gt=0)
    sortino_min: float = Field(gt=0)
    calmar_min: float = Field(gt=0)
    psr_min: float = Field(gt=0)


class ExchangeCfg(BaseModel):
    id: str
    rate_limit: int = Field(gt=0)
    enable_spot: bool


class Config(BaseModel):
    sandbox: SandboxCfg
    metrics: MetricsCfg
    exchanges: list[ExchangeCfg]


# ---------- Helpers ----------


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(path: Path) -> Config:
    data = load_yaml(path)
    return Config.model_validate(data)


# ---------- Tests ----------


CONFIG_PATH = Path(__file__).parents[1] / "configs" / "config.yml"


def test_valid_config():
    cfg = load_config(CONFIG_PATH)

    assert cfg.metrics.sharpe_min >= 1.0
    assert cfg.metrics.sortino_min >= 1.0
    assert cfg.sandbox.cpu_limit <= 2
    assert any(ex.id == "binance" for ex in cfg.exchanges)


def test_invalid_config_raises():
    broken = {
        "sandbox": {"cpu_limit": 0, "memory_limit_mb": 128, "disk_limit_mb": 10, "network": False},
        "metrics": {"sharpe_min": -1, "sortino_min": 0, "calmar_min": 0, "psr_min": 0},
        "exchanges": [{"id": "binance", "rate_limit": -1, "enable_spot": True}],
    }
    with pytest.raises(ValidationError):
        Config.model_validate(broken)

