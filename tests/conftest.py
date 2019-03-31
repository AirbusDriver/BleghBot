import pickle
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent.joinpath('data')


@pytest.fixture('session')
def data_dir():
    return DATA_DIR


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
