from abc import ABC, abstractmethod
import re
from datetime import datetime

import praw.models.reddit.submission

from blegh_bot.exceptions import InteractionParsingError


def get_media_title(submission):
    """
    Return the title of the media content of the `submission` if available, else return None

    :return: `submission` if it has title available
    """
    try:
        return submission.media['oembed']['title']
    except:
        return None


class Interaction(ABC):
    """
    Interface for the various types of interactions the bot may encounter.

    Abstract Methods
    ----------------
    - `Interaction.from_reddit_object()`: classmethod
    - `Interaction.verify_interaction_type()`: classmethod
    """

    @classmethod
    @abstractmethod
    def from_reddit_object(cls, reddit_object):
        """
        Return an instance of class from a reddit object. Should call `cls.verify_interaction_type(reddit_object)` in
        the function to ensure proper exceptions are raised if  reddit_object` doesn't comply.

        :param reddit_object:
        :type reddit_object:
        :return:
        :rtype:
        """
        pass

    @classmethod
    @abstractmethod
    def verify_interaction_type(cls, reddit_object):
        """
        Return `reddit_object`, pass-through, if the :class:`Interaction` subclass is the appropriate response to the
        `reddit_object`, else raise :exception:`InteractionParsingError` if the object does not conform

        :raises InteractionParsingError: if the `reddit_object` is not this type of interaction

        :param reddit_object: any reddit object to check
        :type reddit_object: any
        :return: the `reddit_object`
        """
        pass


class SongSubmission(Interaction):
    """
    Model to represent submissions posted that contain a track posting.

    Interaction Definition
    ----------------------
    * Interaction is a Submission
    * Submission has a song link with a formatted title "artist - track"

    """
    TITLE_RE = re.compile(r'\W?(?P<artist>[\w&\s]*\w)\W?\s*-\s*\W?(?P<track>[\w&\s]*\w)\W?.*', re.IGNORECASE)

    def __init__(self, submission_id, track, artist, shortlink, redditor=None, posted_on_utc=None):
        self.submission_id = submission_id
        self.track = track
        self.artist = artist
        self.redditor = redditor
        self.posted_on_utc = datetime.utcfromtimestamp(posted_on_utc)
        self.shortlink = shortlink

    def __repr__(self):
        s = (f"<{type(self).__name__}(artist: {self.artist}, track: {self.track}, "
             f"posted_on_utc: {self.posted_on_utc!s})>")
        return s

    @classmethod
    def from_reddit_object(cls, reddit_object):
        """
        Return a SongSubmission object from reddit submission. Raises `InteractionParsingError` if `reddit_object`
        does not conform to requirements of `cls.verify_interaction_type` method

        :param reddit_object: reddit submission
        :type reddit_object: praw.models.Submission
        """
        reddit_object = cls.verify_interaction_type(reddit_object)
        parsed_title = cls.TITLE_RE.search(get_media_title(reddit_object))

        return cls(
            submission_id=reddit_object.id,
            track=parsed_title.groupdict()['track'],
            artist=parsed_title.groupdict()['artist'],
            redditor=reddit_object.author.name,
            posted_on_utc=reddit_object.created_utc,
            shortlink=reddit_object.shortlink
        )

    @classmethod
    def verify_interaction_type(cls, reddit_object):
        """
        Raise `InteractionParsingError` if `reddit_object` does not constitute this type of interaction
        """
        if not isinstance(reddit_object, praw.models.reddit.submission.Submission):
            raise InteractionParsingError('not a `Submission` object')

        title = get_media_title(reddit_object)
        if not title:
            raise InteractionParsingError('object has no media')
        else:
            match = cls.TITLE_RE.search(title)
            if not match:
                raise InteractionParsingError(f"{title} does not conform to {cls.TITLE_RE.pattern}")
            return reddit_object
