import unittest
from base_handler import BaseHandler
from datetime import timedelta
from unittest.mock import MagicMock

class TestCreateWithTime(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._keyword = MagicMock()
    self._elapsed = 1
    self._currenttime = MagicMock()
    self._currenttime.strftime = MagicMock(return_value=4)
    
    self._object._current_time = self._currenttime
    
  def tearDown(self):
    pass
    
  def test_advances_time(self):
    self._object._create_with_time(self._keyword, self._elapsed)
    assert(self._object._current_time == (self._currenttime + timedelta(self._elapsed)))
    
if __name__ == '__main__':
  unittest.main()
