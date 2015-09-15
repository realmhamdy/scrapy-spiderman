from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from webpanel.util import generate_models, enumerate_spider_classes
from webpanel.models import Spider


class Command(BaseCommand):

    def handle(self, *args, **options):
        if getattr(settings, "SPIDER_DIRS", None) is None:
            raise ImproperlyConfigured("Required 'SPIDER_DIRS' setting undefined")
        dbspiders = []
        spider_classes = []
        for spider_cls in enumerate_spider_classes():
            self.stdout.write("Found spider '{}' with name '{}'".format(spider_cls.__name__, spider_cls.name))
            dbspiders.append(Spider(name=spider_cls.name))
            spider_classes.append(spider_cls)
        self.stdout.write("Generating item models...")
        generate_models()
        for (dbspider, spider_cls) in zip(dbspiders, spider_classes):
            dbspider.item_model_name = spider_cls.ITEM_CLASS.__name__
            dbspider.save()
