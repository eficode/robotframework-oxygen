import unittest
from oxygen.base_handler import BaseHandler

class TestGetFromTimestamp(unittest.TestCase):
  def setUp(self):
    self._object = BaseHandler()

  def tearDown(self):
    pass

  def test_reads_timestamp(self):
    time_object = self._object._get_from_timestamp('20180203 14:45:10.44')
    assert(time_object.year == 2018)
    assert(time_object.month == 2)
    assert(time_object.day == 3)
    assert(time_object.hour == 14)
    assert(time_object.minute == 45)
    assert(time_object.second == 10)
    assert(time_object.microsecond == 440000)

if __name__ == '__main__':
  unittest.main()
