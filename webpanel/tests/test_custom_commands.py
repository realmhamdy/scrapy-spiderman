from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
import mock
import os.path as pth
from webpanel.management.commands.collect_spiders import Command
from webpanel.models import Spider


class TestCollectSpidersCommand(TestCase):

    @mock.patch("webpanel.management.commands.collect_spiders.settings.SPIDER_DIRS", None, create=True)
    def test_raises_improperlyconfigured(self):
        self.assertRaises(ImproperlyConfigured, Command().handle)

    @mock.patch("webpanel.management.commands.collect_spiders.settings.SPIDER_DIRS",
                [pth.join(pth.dirname(__file__), "test_spiders")], create=True)
    def test_creates_spiders(self):
        command_collect_spiders = Command()
        command_collect_spiders.handle()
        self.assertEqual(Spider.objects.count(), 2)
        self.assertEqual(Spider.objects.filter(item_model_name="CamoformalcrawlerItem").count(), 1)
        self.assertEqual(Spider.objects.filter(item_model_name="SearchdisconnectcrawlerItem").count(), 1)
