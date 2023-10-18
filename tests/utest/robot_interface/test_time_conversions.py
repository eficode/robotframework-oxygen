from unittest import TestCase

from oxygen.robot_interface import RobotInterface


class TestMsToTimestamp(TestCase):
    def setUp(self):
        self.interface = RobotInterface()

    def test_should_be_correct(self):
        timestamp = self.interface.result.ms_to_timestamp(1533625284100.0)
        self.assertEqual(timestamp, '20180807 07:01:24.100000')

        timestamp = self.interface.result.ms_to_timestamp(1533625284451.0)
        self.assertEqual(timestamp, '20180807 07:01:24.451000')

    def test_should_be_associative(self):
        timestamp = '20180807 07:01:24.300000'

        milliseconds = self.interface.result.timestamp_to_ms(timestamp)
        self.assertEqual(milliseconds, 1533625284300.0)

        timestamp = self.interface.result.ms_to_timestamp(milliseconds)
        self.assertEqual(timestamp, '20180807 07:01:24.300000')

        milliseconds = self.interface.result.timestamp_to_ms(timestamp)
        self.assertEqual(milliseconds, 1533625284300.0)

        timestamp = self.interface.result.ms_to_timestamp(milliseconds)
        self.assertEqual(timestamp, '20180807 07:01:24.300000')

    def _validate_timestamp(self, result):
        timestamp = result.ms_to_timestamp(-10)
        expected = '19700101 00:00:00.990000'
        import platform
        # Particular Windows 10 calculates epoch differently ( T ʖ̯ T)
        if platform.system() == 'Windows' and platform.version() == '10.0.19044':
            expected = '19700101 02:00:00.990000'

        self.assertEqual(timestamp, expected)

    def test_ms_before_epoch_are_reset_to_epoch(self):
        from oxygen.robot4_interface import RobotResultInterface as RF4ResultIface
        self._validate_timestamp(RF4ResultIface())

        from oxygen.robot3_interface import RobotResultInterface as RF3ResultIface
        self._validate_timestamp(RF3ResultIface())


class TestTimestampToMs(TestCase):
    def setUp(self):
        self.iface = RobotInterface()

    def test_should_be_correct(self):
        milliseconds = self.iface.result.timestamp_to_ms('20180807 07:01:24.000')
        self.assertEqual(milliseconds, 1533625284000.0)

        milliseconds = self.iface.result.timestamp_to_ms('20180807 07:01:24.555')
        self.assertEqual(milliseconds, 1533625284555.0)

    def test_should_be_associative(self):
        milliseconds = 1533625284300.0

        timestamp = self.iface.result.ms_to_timestamp(milliseconds)
        self.assertEqual(timestamp, '20180807 07:01:24.300000')

        milliseconds = self.iface.result.timestamp_to_ms(timestamp)
        self.assertEqual(milliseconds, 1533625284300.0)

        timestamp = self.iface.result.ms_to_timestamp(milliseconds)
        self.assertEqual(timestamp, '20180807 07:01:24.300000')
