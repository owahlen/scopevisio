from requests import RequestException


class ScopevisioError(RequestException):
    """A Scopevisio specific request error has occured"""
