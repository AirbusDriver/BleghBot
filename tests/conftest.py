from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent.joinpath('data')


@pytest.fixture('session')
def data_dir():
    return DATA_DIR
