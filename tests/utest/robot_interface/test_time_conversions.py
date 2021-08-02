from unittest import TestCase

from oxygen.robot_interface import RobotInterface


class TestMsToTimestamp(TestCase):
    def setUp(self):
        self.interface = RobotInterface()

    def test_should_be_correct(self):
        timestamp = self.interface.result.ms_to_timestamp(1533625284100.0)
        assert timestamp == '20180807 07:01:24.100000'

        timestamp = self.interface.result.ms_to_timestamp(1533625284451.0)
        assert timestamp == '20180807 07:01:24.451000'

    def test_should_be_associative(self):
        timestamp = '20180807 07:01:24.300000'

        milliseconds = self.interface.result.timestamp_to_ms(timestamp)
        assert milliseconds == 1533625284300.0

        timestamp = self.interface.result.ms_to_timestamp(milliseconds)
        assert timestamp == '20180807 07:01:24.300000'

        milliseconds = self.interface.result.timestamp_to_ms(timestamp)
        assert milliseconds == 1533625284300.0

        timestamp = self.interface.result.ms_to_timestamp(milliseconds)
        assert timestamp == '20180807 07:01:24.300000'


class TestTimestampToMs(TestCase):
    def setUp(self):
        self.iface = RobotInterface()

    def test_should_be_correct(self):
        milliseconds = self.iface.result.timestamp_to_ms('20180807 07:01:24.000')
        assert milliseconds == 1533625284000.0

        milliseconds = self.iface.result.timestamp_to_ms('20180807 07:01:24.555')
        assert milliseconds == 1533625284555.0

    def test_should_be_associative(self):
        milliseconds = 1533625284300.0

        timestamp = self.iface.result.ms_to_timestamp(milliseconds)
        assert timestamp == '20180807 07:01:24.300000'

        milliseconds = self.iface.result.timestamp_to_ms(timestamp)
        assert milliseconds == 1533625284300.0

        timestamp = self.iface.result.ms_to_timestamp(milliseconds)
        assert timestamp == '20180807 07:01:24.300000'
