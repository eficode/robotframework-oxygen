import unittest
from base_handler import BaseHandler
from unittest.mock import MagicMock

class TestKeywordsStatus(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._first = MagicMock()
    self._second = MagicMock()
    self._third = MagicMock()
    
    self._first.passed = True
    self._second.passed = False
    self._third.passed = True
    
  def tearDown(self):
    pass
    
  def test_pass(self):
    results = self._object._keywords_status([self._first, self._third])
    assert(results == 'PASS')
    
  def test_fail(self):
    results = self._object._keywords_status([self._first, self._second, self._third])
    assert(results == 'FAIL')
    
if __name__ == '__main__':
  unittest.main()
