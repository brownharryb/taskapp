
class GeoTaskException(Exception):
    pass


class EmptyAddressException(GeoTaskException):
    """Raise when empty address inputted."""

class NoLocationFoundException(GeoTaskException):
    """Raise when no location is found from GeoObject fetch."""


class LocationBoundsUnavailable(GeoTaskException):
    """Raise when bounds are not specified from GeoObject fetch."""


class LocationPositionNotSpecified(GeoTaskException):
    """Raise when position not specified from GeoObject fetch."""


class RemoteResponseException(GeoTaskException):
    """Raise when response status code is not 200."""


class InvalidAddressFormatException(GeoTaskException):
    """Raise when inputted address does not match expected format."""
