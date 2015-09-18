from unittest import TestCase
import os
from os import path as pth
import sys
import mock
from spiderman.util import find_spider_projects
from spiderman.util import generate_item_models, erase_models, enumerate_spider_classes
from spiderman.models import SpiderProject


class TestModelGenerator(TestCase):

    @mock.patch("spiderman.util.settings.SPIDER_DIRS", [pth.join(pth.dirname(__file__), "test_spiders")],
                create=True)
    def test_generate_models(self):
        find_spider_projects()
        generate_item_models()
        from .. import models
        self.assertTrue(hasattr(models, "CamoformalcrawlerItem"))
        self.assertTrue(hasattr(models, "SearchdisconnectcrawlerItem"))
        erase_models()
        self._delete_projects()

    @mock.patch("spiderman.util.settings.SPIDER_DIRS",
                       [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_find_spiders(self):
        modules_before = sys.modules
        find_spider_projects()
        self.assertEqual(SpiderProject.objects.count(), 2)
        self.assertEqual(SpiderProject.objects.filter(path__icontains="camoformal").count(), 1)
        self.assertEqual(SpiderProject.objects.filter(path__icontains="searchdisconnect").count(), 1)
        modules_after = sys.modules
        self.assertEqual(modules_before, modules_after)
        self._delete_projects()

    @mock.patch("spiderman.util.settings.SPIDER_DIRS",
                       [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_enumerate_spiders(self):
        find_spider_projects()
        cwd_before = os.getcwd()
        spider_cls_names = [cls.__name__ for (proj, cls) in enumerate_spider_classes()]
        self.assertIn("CamoformalSpider", spider_cls_names)
        self.assertIn("SearchdisconnectSpider", spider_cls_names)
        self.assertEqual(os.getcwd(), cwd_before)
        self._delete_projects()

    @mock.patch("spiderman.util.settings.SPIDER_DIRS", [], create=True)
    def test_find_no_spiders(self):
        self.assertEqual(len(find_spider_projects()), 0)

    def _delete_projects(self):
        [o.delete() for o in SpiderProject.objects.all()]