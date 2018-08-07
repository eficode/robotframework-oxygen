import unittest
from oxygen import RobotInterface

class TestTimestampToMs(unittest.TestCase):
  def setUp(self):
    self._object = RobotInterface()


  def test_should_be_correct(self):
    milliseconds = self._object.timestamp_to_ms('20180807 07:01:24.000')
    assert milliseconds == 1533625284000.0

    milliseconds = self._object.timestamp_to_ms('20180807 07:01:24.555')
    assert milliseconds == 1533625284555.0
    
    
  def test_should_be_associative(self):
    milliseconds = 1533625284300.0
    
    timestamp = self._object.ms_to_timestamp(milliseconds)
    assert timestamp == '20180807 07:01:24.300000'
    
    milliseconds = self._object.timestamp_to_ms(timestamp)
    assert milliseconds == 1533625284300.0
    
    timestamp = self._object.ms_to_timestamp(milliseconds)
    assert timestamp == '20180807 07:01:24.300000'
    

if __name__ == '__main__':
  unittest.main()
