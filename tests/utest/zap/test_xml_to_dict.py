from unittest import TestCase
from xml.etree import ElementTree as ET

from oxygen.zap import ZAProxyHandler
from ..helpers import get_config


class TestXmlToDict(TestCase):
    def _create_example_xml(self):
        xml_head = ET.Element('xml_head')
        xml_container = ET.SubElement(xml_head, 'xml_container')
        ET.SubElement(xml_head, 'second_child')
        ET.SubElement(xml_container, 'first_contained')
        ET.SubElement(xml_container, 'second_contained')
        return xml_head

    def setUp(self):
        self.object = ZAProxyHandler(get_config()['oxygen.zap'])
        self._xml = self._create_example_xml()

    def test_converts_xml(self):
        returned_dict = self.object._xml_to_dict(self._xml)
        assert('xml_head' in returned_dict)
        assert('xml_container' in returned_dict['xml_head'])
        assert('second_child' in returned_dict['xml_head'])
        assert('first_contained' in returned_dict['xml_head']['xml_container'])
        assert('second_contained' in returned_dict['xml_head']['xml_container'])
