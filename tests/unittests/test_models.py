from unittest.mock import Mock, MagicMock, patch

import pytest

from blegh_bot import models
from blegh_bot.exceptions import InteractionParsingError


class TestGetMediaTitle:
    @pytest.mark.parametrize('submission_index', [
        3,
    ])
    def test_get_media_title_returns_submission_when_has_media(self, submission_index, unpickled_submissions):
        submission = unpickled_submissions[submission_index]
        assert models.get_media_title(submission)


class TestSongSubmissionInteraction:
    def test_submission_init_holds_submission_object(self, unpickled_submissions):
        song_submission = models.SongSubmission(unpickled_submissions[3])
        assert isinstance(song_submission, models.SongSubmission)
        assert song_submission.submission is unpickled_submissions[3]

    @pytest.mark.parametrize('submission_index, should_pass', [
        pytest.param(0, False, id='weekly rec submission raises'),
        pytest.param(3, True, id='youtube link passes'),
        pytest.param(4, False, id='text submission raises'),
        pytest.param(18, True, id='youtube link with symbol')
    ])
    def test_verify_interaction_type_returns_for_appropriate_link_types(self, submission_index, should_pass,
                                                                        unpickled_submissions):
        submission = unpickled_submissions[submission_index]
        if should_pass:
            result = models.SongSubmission.verify_interaction_type(submission)
            assert result is submission
        else:
            with pytest.raises(InteractionParsingError):
                models.SongSubmission.verify_interaction_type(submission)
