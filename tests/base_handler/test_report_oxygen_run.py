import unittest
from base_handler import BaseHandler
from unittest.mock import MagicMock

class TestReportOxygenRun(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._object._robot_keyword = MagicMock(return_value=None)
    self._object._build_results = MagicMock()
    
  def tearDown(self):
    pass
    
  def test_call_propagates(self):
    self._object._report_oxygen_run('Keyword', [], [])
    assert(self._object._robot_keyword.call_count == 2)
    self._object._build_results.assert_called_once_with('Keyword', None, None)
    
if __name__ == '__main__':
  unittest.main()
