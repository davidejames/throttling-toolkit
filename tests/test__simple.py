import pytest

from throttling_toolkit.simple import(
    ThrottlingError,
    throttle,
    Defaults,
)


def test__basic():

    @throttle()
    def foo():
        pass


def test__throttling():
    current_time = 0
    def _fake_time_f():
        nonlocal current_time
        current_time += 0.1
        return current_time

    _save_time_f = Defaults.TIME_FUNC
    Defaults.TIME_FUNC = _fake_time_f

    @throttle()
    def foo():
        pass

    # we should see throttling at 6th call:
    with pytest.raises(ThrottlingError):
        for n in range(10):
            foo()

    Defaults.TIME_FUNC = _save_time_f

    # range starts at 0, so for 6th call n will be 5
    assert n == 5
