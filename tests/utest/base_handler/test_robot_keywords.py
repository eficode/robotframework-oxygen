import unittest
from base_handler import BaseHandler
from unittest.mock import MagicMock

class TestRobotKeywords(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._object._robot_keyword = MagicMock()
    self._keywords = [MagicMock(), MagicMock(), MagicMock()]
    self._kwarg = MagicMock()
    
  def tearDown(self):
    pass
    
  def test_converts_all(self):
    self._object._robot_keywords(*self._keywords, mockarg=self._kwarg)
    for keyword in self._keywords:
      self._object._robot_keyword.assert_any_call(existing=keyword, mockarg=self._kwarg)
    assert(self._object._robot_keyword.call_count == len(self._keywords))
    
if __name__ == '__main__':
  unittest.main()
