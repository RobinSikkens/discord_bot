""" Contains a wrapper to support multiple return types. """


class Response:
    """ Bot response wrapper. """

    message = None
    embed = None
    files = None
    delete_after = None
