from datetime import datetime, timedelta, tzinfo
from calendar import timegm

EPOCH_AS_FILETIME = 116444736000000000
HUNDREDS_OF_NANOSECONDS = 10000000

ZERO = timedelta(0)
HOUR = timedelta(hours=1)


class UTC(tzinfo):

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


def dt_to_filetime(dt):
    if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
        dt = dt.replace(tzinfo=utc)
    return EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)


def filetime_to_dt(ft):
    return datetime.fromtimestamp((ft - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS, tz=utc)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
