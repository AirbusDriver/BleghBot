import pytest

from pytest_bdd import given, then, scenario

from blegh_bot.models import SongSubmission, InteractionParsingError


@scenario('../features/interaction_parsing.feature', 'Song posts are identified')
def test_song_post_identified():
    pass


@scenario('../features/interaction_parsing.feature', 'All song posts are identified',
          example_converters=dict(valid=int)
          )
def test_outlined(parsed_interaction):
    pass


@given('There is a <valid> song submission from the feed')
def valid_song_submission_from_the_feed(valid, unpickled_submissions):
    return unpickled_submissions[int(valid)]


@given('A user tries to create a song interaction from it')
def parsed_interaction(valid_song_submission_from_the_feed):
    return SongSubmission.from_reddit_object(valid_song_submission_from_the_feed)


@given('There is a valid song submission')
def valid_song_submission(unpickled_submissions):
    submission = unpickled_submissions[3]
    return submission


@given('There is an invalid song submission', target_fixture=valid_song_submission)
def invalid_song_submission(unpickled_submissions):
    submission = unpickled_submissions[4]
    return submission


@given('The post is parsed')
def parse_post(valid_song_submission):
    interaction = SongSubmission.from_reddit_object(valid_song_submission)
    return interaction


@given('There is a <valid> song submission from the feed')
def valid_song_from_pickled_submissions(valid, unpickled_submissions):
    return unpickled_submissions[int(valid)]


@then('I should have a SongInteraction')
def test_song_interaction_returned(parse_post):
    assert isinstance(parse_post, SongSubmission)


@then('I should be able to see the track information')
def test_attrs(parse_post):
    required_attrs = [
        'artist', 'track', 'redditor', 'submission_id', 'posted_on_utc', 'shortlink'
    ]
    assert all([
        getattr(parse_post, attr) is not None for attr in required_attrs
    ])


@then('I should see an InteractionParsingError upon parsing')
def test_raises_interaction_parsing_error(invalid_song_submission):
    with pytest.raises(InteractionParsingError) as exc_info:
        SongSubmission.from_reddit_object(invalid_song_submission)
