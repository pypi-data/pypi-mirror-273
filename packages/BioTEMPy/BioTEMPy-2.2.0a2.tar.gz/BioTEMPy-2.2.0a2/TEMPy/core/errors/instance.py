class BaseError(Exception):
    """ Base class for all Exceptions """


class InstanceError(BaseError):
    """ An incorrect instance was passed """
