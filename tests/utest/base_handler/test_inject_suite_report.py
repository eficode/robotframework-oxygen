import unittest
from oxygen.base_handler import BaseHandler
from unittest.mock import MagicMock

class TestInjectSuiteReport(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._test = MagicMock()
    self._parent = MagicMock()
    self._traveller = MagicMock()
    self._suites = MagicMock()
    self._suites.append = MagicMock()
    self._suite = MagicMock()

    self._test.parent = self._parent
    self._parent.tests = [1, 2, self._test, 3]
    self._parent.parent = self._traveller
    self._traveller.parent = None
    self._traveller.suites = self._suites

  def tearDown(self):
    pass

  def test_finds_and_appends(self):
    self._object._inject_suite_report(self._test, self._suite)
    self._suites.append.assert_called_once_with(self._suite)

  def test_finds_and_filters(self):
    self._object._inject_suite_report(self._test, self._suite)
    assert(self._parent.tests == [1, 2, 3])

if __name__ == '__main__':
  unittest.main()
