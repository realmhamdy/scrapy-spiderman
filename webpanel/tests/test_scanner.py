__author__ = 'Mohammed Hamdy'

from unittest import TestCase
from os import path as pth
import sys
import mock
from webpanel.spider_finder import find_spiders


class TestSpiderScan(TestCase):

    @mock.patch("webpanel.spider_finder.settings.SPIDER_DIRS",
                       [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_find_spiders(self):
        modules_before = sys.modules
        settings_modules = find_spiders()
        self.assertEqual(len(settings_modules), 2)
        modules_after = sys.modules
        self.assertEqual(modules_before, modules_after)

    @mock.patch("webpanel.spider_finder.settings.SPIDER_DIRS", [], create=True)
    def test_find_no_spiders(self):
        self.assertEqual(len(find_spiders()), 0)
