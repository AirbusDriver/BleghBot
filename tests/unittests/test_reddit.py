from unittest.mock import Mock, MagicMock, patch

import pytest

from blegh_bot import reddit


@pytest.mark.usefixtures('sample_config')
class TestAuthorizeReddit:
    def test_authorize_reddit(self, sample_config):
        with patch('blegh_bot.reddit.praw') as mock_praw:
            red = reddit.authorize_reddit(**sample_config['reddit'])
        mock_praw.Reddit.assert_called_with(**sample_config['reddit'])
