from unittest import TestCase
from unittest.mock import MagicMock

from oxygen.base_handler import BaseHandler
from ..helpers import get_config


class TestInjectSuiteReport(TestCase):
    def setUp(self):
        self.handler = BaseHandler(get_config()['oxygen.junit'])

        self.test = MagicMock()
        self.parent = MagicMock()
        self.traveller = MagicMock()
        self.suites = MagicMock()
        self.suites.append = MagicMock()
        self.suite = MagicMock()

        self.test.parent = self.parent
        self.parent.tests = [1, 2, self.test, 3]
        self.parent.parent = self.traveller
        self.traveller.parent = None
        self.traveller.suites = self.suites

    def test_finds_and_appends(self):
        self.handler._inject_suite_report(self.test, self.suite)
        self.test.parent.suites.append.assert_called_once_with(self.suite)

    def test_finds_and_filters(self):
        self.handler._inject_suite_report(self.test, self.suite)
        self.assertEqual(self.parent.tests, [1, 2, 3])
