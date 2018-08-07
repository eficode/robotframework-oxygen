import unittest
from oxygen import RobotInterface

class TestMsToTimestamp(unittest.TestCase):
  def setUp(self):
    self._object = RobotInterface()


  def test_should_be_correct(self):
    timestamp = self._object.ms_to_timestamp(1533625284100.0)
    assert timestamp == '20180807 07:01:24.100000'

    timestamp = self._object.ms_to_timestamp(1533625284451.0)
    assert timestamp == '20180807 07:01:24.451000'
    
    
  def test_should_be_associative(self):
    timestamp = '20180807 07:01:24.300000'
    
    milliseconds = self._object.timestamp_to_ms(timestamp)
    assert milliseconds == 1533625284300.0
    
    timestamp = self._object.ms_to_timestamp(milliseconds)
    assert timestamp == '20180807 07:01:24.300000'
    
    milliseconds = self._object.timestamp_to_ms(timestamp)
    assert milliseconds == 1533625284300.0
    
    timestamp = self._object.ms_to_timestamp(milliseconds)
    assert timestamp == '20180807 07:01:24.300000'
    

if __name__ == '__main__':
  unittest.main()
