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


def print_result(value: Result):
    print()
    print(f'elapsed:{value.elapsed.total_milli_seconds()} recent:{value.recent} current:{value.current}')


class TestMonotonicChronograph:

    def test_initial_state(self):
        tmp = MonotonicChronograph()
        assert_result(tmp.elapsed(), TimeSpan(0), Status.RESET, Status.RESET)

    def test_start(self):
        print()
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
        assert_result(tmp.stop(), TimeSpan(0), Status.RESET, Status.RESET)

        with mock.patch('time.monotonic_ns') as monotonic:
            monotonic.return_value = 1600
            assert_result(tmp.start(), TimeSpan(0), Status.RESET, Status.RUNNING)
            assert monotonic.call_count == 1

            monotonic.return_value = 1800
            assert_result(tmp.stop(), TimeSpan(200), Status.RUNNING, Status.STOPPED)
            assert monotonic.call_count == 2

            foo = tmp.stop()
            print_result(foo)
            assert_result(tmp.stop(), TimeSpan(200), Status.STOPPED, Status.STOPPED)

    def test_restart(self):
        tmp = MonotonicChronograph()
        with mock.patch('time.monotonic_ns') as monotonic:
            assert monotonic.call_count == 0
            monotonic.return_value = 1600
            assert_result(tmp.restart(), TimeSpan(0), Status.RESET, Status.RUNNING)
            assert monotonic.call_count == 1

            monotonic.return_value = 1700
            assert_result(tmp.restart(), TimeSpan(100), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 3

            monotonic.return_value = 2000
            assert_result(tmp.restart(), TimeSpan(300), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 5

    def test_reset(self):
        tmp = MonotonicChronograph()

        with mock.patch('time.monotonic_ns') as monotonic:
            assert_result(tmp.reset(), TimeSpan(0), Status.RESET, Status.RESET)
            assert monotonic.call_count == 0

            monotonic.return_value = 1600
            tmp.start()
            assert monotonic.call_count == 1

            monotonic.return_value = 1800
            assert_result(tmp.reset(), TimeSpan(200), Status.RUNNING, Status.RESET)

            assert monotonic.call_count == 2

            monotonic.return_value = 2000

            assert_result(tmp.reset(), TimeSpan(0), Status.RESET, Status.RESET)
            assert monotonic.call_count == 2

    def test_elapsed(self):
        tmp = MonotonicChronograph()

        with mock.patch('time.monotonic_ns') as monotonic:
            assert_result(tmp.elapsed(), TimeSpan(0), Status.RESET, Status.RESET)
            assert monotonic.call_count == 0

            monotonic.return_value = 1600
            tmp.start()
            monotonic.return_value = 1800
            assert_result(tmp.elapsed(), TimeSpan(200), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 2

            monotonic.return_value = 2200
            assert_result(tmp.elapsed(), TimeSpan(600), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 3

            monotonic.return_value = 2500
            tmp.stop()
            assert_result(tmp.elapsed(), TimeSpan(900), Status.STOPPED, Status.STOPPED)

    def test_cumulative(self):
        tmp = MonotonicChronograph()

        with mock.patch('time.monotonic_ns') as monotonic:
            assert_result(tmp.elapsed(), TimeSpan(0), Status.RESET, Status.RESET)
            assert monotonic.call_count == 0

            monotonic.return_value = 1600
            assert_result(tmp.start(), TimeSpan(0), Status.RESET, Status.RUNNING)
            assert monotonic.call_count == 1

            monotonic.return_value = 1800
            assert_result(tmp.elapsed(), TimeSpan(200), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 2

            monotonic.return_value = 2200
            assert_result(tmp.stop(), TimeSpan(600), Status.RUNNING, Status.STOPPED)
            assert monotonic.call_count == 3

            monotonic.return_value = 2500
            assert_result(tmp.stop(), TimeSpan(600), Status.STOPPED, Status.STOPPED)
            assert_result(tmp.elapsed(), TimeSpan(600), Status.STOPPED, Status.STOPPED)
            assert monotonic.call_count == 3

            monotonic.return_value = 5000
            assert_result(tmp.start(), TimeSpan(600), Status.STOPPED, Status.RUNNING)
            assert monotonic.call_count == 4

            monotonic.return_value = 6000
            assert_result(tmp.elapsed(), TimeSpan(1600), Status.RUNNING, Status.RUNNING)
            assert monotonic.call_count == 5

            monotonic.return_value = 7500
            assert_result(tmp.stop(), TimeSpan(3100), Status.RUNNING, Status.STOPPED)
            assert_result(tmp.elapsed(), TimeSpan(3100), Status.STOPPED, Status.STOPPED)
            assert monotonic.call_count == 6
