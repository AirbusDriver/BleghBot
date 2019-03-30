import praw
import prawcore.exceptions


class AuthorizationError(Exception):
    pass


def authorize_reddit(**reddit_credentials):
    """
    Return a `praw.Reddit` an authorized instance.

    :param reddit_credentials: credentials required for :class:`praw.Reddit` authorization
    :rtype: praw.Reddit
    """
    try:
        reddit = praw.Reddit(**reddit_credentials)
        reddit.user.me()
        return reddit
    except (prawcore.exceptions.ResponseException, prawcore.exceptions.OAuthException):
        raise AuthorizationError(f'error authorizing Reddit instance with credentials {reddit_credentials}')
