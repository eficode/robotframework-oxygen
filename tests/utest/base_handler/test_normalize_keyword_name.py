import unittest
from oxygen.base_handler import BaseHandler
from yaml import load

class TestNormalizeKeywordName(unittest.TestCase):
  def setUp(self):
    with open('../config.yml', 'r') as infile:
      self._config = load(infile)
      self._object = BaseHandler(self._config['oxygen.zap'])

  def test_normalize(self):
    normalized = self._object._normalize_keyword_name('Suite 1 . Suite 2 . My KeyWord NAME   ')
    assert(normalized == 'my_keyword_name')

if __name__ == '__main__':
  unittest.main()
