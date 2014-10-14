from datetime import datetime
from datetime import tzinfo, timedelta


def convert_to_dtype(v, dtype):
    """Convert v to a python datetime if dtype is 'datetime'"""
    if dtype == 'datetime':
        utc = UTC()
        if isinstance(v, list):
            return [datetime.fromtimestamp(value, tz=utc) for value in v]
        else:
            return datetime.fromtimestamp(v, tz=utc)
    return v


# A UTC class.
# From https://docs.python.org/2/library/datetime.html#tzinfo-objects
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


