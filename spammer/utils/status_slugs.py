from enum import Enum

__all__ = ['AuthStatusSlug', 'SpammerStatusSlug']


class AuthStatusSlug(Enum):
    ERROR = 0
    CODE_SEND = 1
    CODE_VERIFIED = 2
    AUTH_SUCCESS = 3


class SpammerStatusSlug(Enum):
    BANNED_CHAT = 1
    BANNED_ACCOUNT = 2
    UNKNOWN_ERROR = 3
    OK = 3
