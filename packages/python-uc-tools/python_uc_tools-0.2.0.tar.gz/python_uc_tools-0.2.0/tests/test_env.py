from dataclasses import dataclass

import pytest
from uc_tools import BaseConfig, Env


@dataclass
class MockGoodConfig(BaseConfig):
    test: str


@dataclass
class MockBadConfig(BaseConfig):
    no_field: str


def test_good_settings():
    settings: MockGoodConfig = Env.load(env_name='test_env.txt', config=MockGoodConfig)
    assert settings.test == 'hello'


def test_bad_settings():
    with pytest.raises(ValueError):
        Env.load(env_name='test_env.txt', config=MockBadConfig)
