from unittest import TestCase
from os import path as pth
import sys
import mock
from webpanel.util import find_spiders
from webpanel.util import generate_models, erase_models


class TestModelGenerator(TestCase):

    @mock.patch("webpanel.util.settings.SPIDER_DIRS", [pth.join(pth.dirname(__file__), "test_spiders")],
                create=True)
    def test_generate_models(self):
        generate_models()
        from .. import models
        self.assertTrue(hasattr(models, "CamoformalcrawlerItem"))
        self.assertTrue(hasattr(models, "SearchdisconnectcrawlerItem"))
        erase_models()

    @mock.patch("webpanel.util.settings.SPIDER_DIRS",
                       [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_find_spiders(self):
        modules_before = sys.modules
        settings_modules = find_spiders()
        self.assertEqual(len(settings_modules), 2)
        modules_after = sys.modules
        self.assertEqual(modules_before, modules_after)

    @mock.patch("webpanel.util.settings.SPIDER_DIRS", [], create=True)
    def test_find_no_spiders(self):
        self.assertEqual(len(find_spiders()), 0)
