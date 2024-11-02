import time
import functools


class ThrottlingError(Exception):
    pass


def throttle(max_rate=5):

    def decorator(func):

        call_rate = 0
        prev_call_time = time.time()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            call_rate      += 1
            now             = time.time()
            call_rate       = max(0, call_rate - (now - prev_call_time))
            prev_call_time  = now

            if call_rate > max_rate:
                raise ThrottlingError()

            return func(*args, **kwargs)

        return wrapper

    return decorator
