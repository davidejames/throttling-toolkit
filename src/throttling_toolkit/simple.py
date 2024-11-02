import time
import functools


class Defaults:
    TIME_FUNC = time.time

class ThrottlingError(Exception):
    pass


def throttle(max_rate=5):

    def decorator(func):

        call_rate = 0
        prev_call_time = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_rate
            nonlocal prev_call_time

            now = Defaults.TIME_FUNC()

            if prev_call_time is None:
                prev_call_time = now

            call_rate      += 1
            call_rate       = max(0, call_rate - (now - prev_call_time))
            prev_call_time  = now

            if call_rate > max_rate:
                raise ThrottlingError()

            return func(*args, **kwargs)

        return wrapper

    return decorator
