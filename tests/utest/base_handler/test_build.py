import unittest
from base_handler import BaseHandler

class TestBuild(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()
    
  def test_build(self):
    config = {'keyword': 'suite.suite.A B C', 'tags': 5}
    self._object.build(config)
    
    self.assertTrue(self._object._config == config)
    self.assertTrue(self._object._keyword == 'a_b_c')
    self.assertTrue(self._object._tags == [5])
    
if __name__ == '__main__':
  unittest.main()
