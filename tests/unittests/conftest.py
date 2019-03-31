import pytest

from blegh_bot.constants import BASE_DIR


@pytest.fixture
def use_sample_config_yaml(monkeypatch):
    """Override the CONFIG_FILE constant in constants.py to drive the config to use the sample_config.yaml file"""
    monkeypatch.setattr('blegh_bot.constants.CONFIG_FILE', BASE_DIR.joinpath('sample_config.yaml'))


@pytest.fixture(scope='function')
def sample_config(use_sample_config_yaml):
    from blegh_bot.config import file_config
    return file_config


