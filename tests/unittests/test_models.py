from datetime import datetime

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

    def test_from_reddit_object_returns_parsed_song_submission(self, unpickled_submissions):
        submission = unpickled_submissions[3]
        result = models.SongSubmission.from_reddit_object(submission)

        assert result.artist == 'Periphery'
        assert result.track == 'Facepalm Mute'
        assert result.redditor == 'mullen711'
        assert result.submission_id == 'b7l3pq'
        assert result.posted_on_utc == datetime.utcfromtimestamp(1554016786)
        assert result.shortlink == 'https://redd.it/b7l3pq'
