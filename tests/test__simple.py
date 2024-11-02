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


def test__throttling__1():
    current_time = 0
    def _fake_time_f():
        nonlocal current_time
        current_time += 0.1
        return current_time

    @throttle()
    def foo():
        pass

    _save_time_f = Defaults.TIME_FUNC
    Defaults.TIME_FUNC = _fake_time_f

    n = 0
    try:
        # we should see throttling at 6th call:
        with pytest.raises(ThrottlingError):
            for n in range(10):
                print(f'n={n}, time={current_time}')
                foo()
                print(f'n={n}, time={current_time}')

    except Exception as e:
        raise

    finally:
        Defaults.TIME_FUNC = _save_time_f

    # range starts at 0, so for 6th call n will be 5
    assert n == 5


def test__throttling__2():
    current_time = 0
    def _fake_time_f():
        nonlocal current_time
        current_time += 0.1
        return current_time

    @throttle()
    def foo():
        pass

    _save_time_f = Defaults.TIME_FUNC
    Defaults.TIME_FUNC = _fake_time_f

    try:
        for n in range(5):
            foo()

        current_time += 5

        for n in range(5):
            foo()

    finally:
        Defaults.TIME_FUNC = _save_time_f



def test__throttling__3():
    current_time = 0
    def _fake_time_f():
        nonlocal current_time
        current_time += 0.1
        return current_time

    @throttle()
    def foo():
        pass

    _save_time_f = Defaults.TIME_FUNC
    Defaults.TIME_FUNC = _fake_time_f

    try:
        # we should see throttling at 6th call:
        with pytest.raises(ThrottlingError):
            for n in range(10):
                foo()
    finally:
        Defaults.TIME_FUNC = _save_time_f

    # range starts at 0, so for 6th call n will be 5
    assert n == 5
