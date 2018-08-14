import unittest
import xml.etree.ElementTree as ET
from oxygen.zap import ZAProxyHandler
from unittest.mock import MagicMock
from yaml import load

class TestXmlToDict(unittest.TestCase):
    def setUp(self):
        with open('../config.yml', 'r') as infile:
            self._config = load(infile)
            self._object = ZAProxyHandler(self._config['oxygen.zap'])

        xml_head = ET.Element('xml_head')
        xml_container = ET.SubElement(xml_head, 'xml_container')
        ET.SubElement(xml_head, 'second_child')
        ET.SubElement(xml_container, 'first_contained')
        ET.SubElement(xml_container, 'second_contained')
        self._xml = xml_head

    def tearDown(self):
        pass

    def test_converts_xml(self):
        returned_json = self._object._xml_to_dict(self._xml)
        assert('xml_head' in returned_json)
        assert('xml_container' in returned_json['xml_head'])
        assert('second_child' in returned_json['xml_head'])
        assert('first_contained' in returned_json['xml_head']['xml_container'])
        assert('second_contained' in returned_json['xml_head']['xml_container'])

    if __name__ == '__main__':
        unittest.main()
