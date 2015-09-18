from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from spiderman.util import generate_item_models, enumerate_spider_classes, find_spider_projects
from spiderman.models import Spider, SpiderProject


class Command(BaseCommand):

    def handle(self, *args, **options):
        if getattr(settings, "SPIDER_DIRS", None) is None:
            raise ImproperlyConfigured("Required 'SPIDER_DIRS' setting undefined")
        dbspiders = []
        spider_classes = []
        find_spider_projects()
        if SpiderProject.objects.count() == 0:
            self.stdout.write("Found no projects. Please recheck your 'SPIDER_DIRS' setting and/or projects")
            return
        for spider_project, spider_cls in enumerate_spider_classes():
            self.stdout.write("\nFound spider '{}' with name '{}'".format(spider_cls.__name__, spider_cls.name))
            dbspiders.append(Spider(name=spider_cls.name, project=spider_project))
            spider_classes.append(spider_cls)
        self.stdout.write("\nGenerating item models...")
        generate_item_models()
        self.stdout.write("\nDone generating item models")
        for (dbspider, spider_cls) in zip(dbspiders, spider_classes):
            dbspider.item_model_name = spider_cls.ITEM_CLASS.__name__
            dbspider.save()
        self.stdout.write("\nDone")
