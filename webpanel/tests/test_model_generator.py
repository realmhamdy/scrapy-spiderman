from unittest import TestCase
import os.path as pth
import mock
from webpanel.util import generate_models, erase_models


class TestModelGenerator(TestCase):

    @mock.patch("webpanel.spider_finder.settings.SPIDER_DIRS", [pth.join(pth.dirname(__file__), "test_spiders")],
                create=True)
    def test_generate_models(self):
        generate_models()
        from .. import models
        self.assertTrue(hasattr(models, "CamoformalcrawlerItem"))
        self.assertTrue(hasattr(models, "SearchdisconnectcrawlerItem"))
        erase_models()
