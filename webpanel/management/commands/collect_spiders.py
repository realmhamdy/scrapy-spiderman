from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from webpanel.util import generate_item_models, enumerate_spider_classes, find_spider_projects
from webpanel.models import Spider


class Command(BaseCommand):

    def handle(self, *args, **options):
        if getattr(settings, "SPIDER_DIRS", None) is None:
            raise ImproperlyConfigured("Required 'SPIDER_DIRS' setting undefined")
        dbspiders = []
        spider_classes = []
        find_spider_projects()
        for spider_project, spider_cls in enumerate_spider_classes():
            self.stdout.write("Found spider '{}' with name '{}'".format(spider_cls.__name__, spider_cls.name))
            dbspiders.append(Spider(name=spider_cls.name, project=spider_project))
            spider_classes.append(spider_cls)
        else:
            self.stdout.write("Found no projects. Please recheck your 'SPIDER_DIRS' setting and/or projects")
            return
        self.stdout.write("Generating item models...")
        generate_item_models()
        for (dbspider, spider_cls) in zip(dbspiders, spider_classes):
            dbspider.item_model_name = spider_cls.ITEM_CLASS.__name__
            dbspider.save()
