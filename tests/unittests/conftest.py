from unittest.mock import MagicMock, Mock, patch
from pathlib import Path
import pickle

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


@pytest.fixture('session')
def unpickled_submissions(data_dir):
    """
    Return a list of 20 reddit submission objects. The vars() information is in the `pickled_submissions.json` file
    in the `data` directory

    :return: list of 20 reddit submission objects
    :rtype: list
    """
    pickle_file = Path(data_dir.joinpath('pickled_submissions'))
    assert pickle_file.exists()
    data = pickle_file.read_bytes()
    return pickle.loads(data)
