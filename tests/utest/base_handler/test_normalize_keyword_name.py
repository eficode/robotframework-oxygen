from unittest import TestCase

from oxygen.base_handler import BaseHandler
from ..helpers import get_config


class TestNormalizeKeywordName(TestCase):

    def test_normalize(self):
        self.bh = BaseHandler(get_config()['oxygen.gatling'])
        unnormalized = 'Suite 1 . Suite 2 . My KeyWord NAME   '
        self.assertEqual(self.bh._normalize_keyword_name(unnormalized),
                         'my_keyword_name')
