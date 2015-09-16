from unittest import TestCase
from os import path as pth
import sys
import mock
from webpanel.util import find_spider_projects
from webpanel.util import generate_item_models, erase_models


class TestModelGenerator(TestCase):

    @mock.patch("webpanel.util.settings.SPIDER_DIRS", [pth.join(pth.dirname(__file__), "test_spiders")],
                create=True)
    def test_generate_models(self):
        generate_item_models()
        from .. import models
        self.assertTrue(hasattr(models, "CamoformalcrawlerItem"))
        self.assertTrue(hasattr(models, "SearchdisconnectcrawlerItem"))
        erase_models()

    @mock.patch("webpanel.util.settings.SPIDER_DIRS",
                       [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_find_spiders(self):
        modules_before = sys.modules
        spider_projects = find_spider_projects()
        self.assertEqual(len(spider_projects), 2)
        modules_after = sys.modules
        self.assertEqual(modules_before, modules_after)

    @mock.patch("webpanel.util.settings.SPIDER_DIRS", [], create=True)
    def test_find_no_spiders(self):
        self.assertEqual(len(find_spider_projects()), 0)
