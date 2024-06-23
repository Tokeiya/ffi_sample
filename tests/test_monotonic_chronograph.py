from chrono.timespan import TimeSpan
from chrono.monotonic_chronograph import MonotonicChronograph
import unittest.mock as mock
from pytest import fixture
from chrono.chronograph_status import Status
from chrono.chronograph_result import Result
import time


def assert_result(actual: Result, elapsed: TimeSpan, recent: Status, current: Status):
    assert actual.elapsed == elapsed
    assert actual.recent == recent
    assert actual.current == current


class TestMonotonicChronograph:

    @fixture
    def init_fixture(self) -> MonotonicChronograph:
        return MonotonicChronograph()

    def test_initial_state(self, init_fixture: MonotonicChronograph):
        assert init_fixture.status() == Status.RESET
        assert_result(init_fixture.elapsed(), TimeSpan(0), Status.RESET, Status.RESET)

    def test_start(self):
        tmp = MonotonicChronograph()
        with mock.patch('time.monotonic_ns') as monotonic:
            monotonic.return_value = 1500
            assert_result(tmp.start(), TimeSpan(0), Status.RESET, Status.RUNNING)
            monotonic.return_value = 1600
            assert_result(tmp.start(), TimeSpan(100), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 2
            assert tmp.status() == Status.RUNNING

    def test_stop(self):
        tmp = MonotonicChronograph()
        with mock.patch('time.monotonic_ns') as monotonic:
            assert_result(tmp.stop(), TimeSpan(0), Status.RESET, Status.RESET)
            assert monotonic.call_count == 0
            monotonic.time.return_value = 1600
            tmp.start()

            monotonic.return_value = 1700
            assert_result(tmp.stop(), TimeSpan(100), Status.STOPPED, Status.STOPPED)
            assert monotonic.call_count == 2

            assert_result(tmp.stop(), TimeSpan(100), Status.STOPPED, Status.STOPPED)

    def test_restart(self):
        assert False

    def test_reset(self):
        assert False

    def test_elapsed(self):
        assert False
