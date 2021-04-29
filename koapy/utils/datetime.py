def is_naive(dt):
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def localize(dt, tz):
    if is_naive(dt):
        dt = tz.localize(dt)
    else:
        dt = dt.astimezone(tz)
    return dt
