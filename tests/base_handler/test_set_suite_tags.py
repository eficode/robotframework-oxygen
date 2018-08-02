import unittest
from base_handler import BaseHandler
from unittest.mock import MagicMock

class TestSetSuiteTags(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    self._suite = MagicMock()
    self._suite.set_tags = MagicMock()
    self._tags = (MagicMock(), MagicMock())
    
  def tearDown(self):
    pass
    
  def test_tags_are_set(self):
    self._object._set_suite_tags(self._suite, *self._tags)
    self._suite.set_tags.assert_called_once_with(self._tags)
    
if __name__ == '__main__':
  unittest.main()
