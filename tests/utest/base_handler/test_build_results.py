import unittest
from oxygen.base_handler import BaseHandler
from unittest.mock import MagicMock

class TestBuildResults(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._results = MagicMock()
    self._result_suite = MagicMock()
    self._append = MagicMock()

    self._object._parse_results = MagicMock(return_value=self._results)
    self._object._build_suite = MagicMock(return_value=self._result_suite)
    self._object._set_suite_tags = MagicMock()
    self._object._inject_suite_report = MagicMock()

    self._result_suite.keywords = MagicMock()
    self._result_suite.keywords.append = self._append
    self._object._tags = [3, 4]

    self._keyword = MagicMock()
    self._setup = MagicMock()
    self._teardown = MagicMock()

    self._keyword.parent = MagicMock
    self._keyword.parent.tags = [1, 2]

  def tearDown(self):
    pass

  def test_tags_are_set(self):
    self._object._build_results(self._keyword, self._setup, self._teardown)
    self._object._set_suite_tags.assert_called_once_with(self._result_suite, 3, 4, 1, 2)

  def test_setup_teardown_are_included(self):
    self._object._build_results(self._keyword, self._setup, self._teardown)
    self._append.assert_any_call(self._setup)
    self._append.assert_any_call(self._teardown)
    assert(self._append.call_count == 2)

  def test_report_is_injected(self):
    self._object._build_results(self._keyword, self._setup, self._teardown)
    self._object._inject_suite_report.assert_called_once_with(self._keyword.parent, self._result_suite)

if __name__ == '__main__':
  unittest.main()
