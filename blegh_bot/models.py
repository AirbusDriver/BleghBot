from abc import ABC, abstractmethod
import re

import praw.models.reddit.submission

from blegh_bot.exceptions import InteractionError, InteractionParsingError


def get_media_title(submission):
    """Return the title of the media content of the `submission` if available, else return None"""
    try:
        return submission.media['oembed']['title']
    except:
        return None


class Interaction(ABC):

    @classmethod
    @abstractmethod
    def from_reddit_object(self, reddit_object):
        """
        Return an instance of class from a reddit object

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
        Return self if the Interaction subclass is the appropriate response to the `reddit_object`, else raise
        `InteractionParsingError` if the object does not conform

        :param reddit_object:
        :type reddit_object:
        :return:
        :rtype:
        """
        pass


class SongSubmission(Interaction):
    """
    Model to represent submissions posted that contain a track posting.
    """
    TITLE_RE = re.compile(r'(?P<artist>[\w\s]*)\s*-\s*(?P<track>[\w\s]*)', re.IGNORECASE)

    def __init__(self, submission):
        self.submission = submission

    @classmethod
    def from_reddit_object(self, reddit_object):
        pass

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
