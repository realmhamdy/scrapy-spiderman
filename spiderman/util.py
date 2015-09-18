import imp
import os
import os.path as pth
import sys
from imp import reload
from django.conf import settings
from django import setup
from django.core.management import call_command
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
from scrapy.utils.project import get_project_settings, ENVVAR
from cogapp import Cog
from . import models
from .models import SpiderProject
from .models import spider_models


def start_django(**options):
    # this can be used from scripts that need Django functionality
    if not settings.configured:
        settings.configure(**options)
        setup()


def generate_item_models():
    target_file = pth.join(pth.dirname(__file__), "models", "spider_models.py")
    Cog().main([sys.argv[0], "-r", target_file])
    reload(spider_models)
    reload(models)
    call_command("makemigrations")
    call_command("migrate", "spiderman")


def erase_models():
    target_file = pth.join(pth.dirname(__file__), "models", "spider_models.py")
    Cog().main([sys.argv[0], "-x", target_file])


def find_spider_projects():
    # Creates SpiderProject objects for found Scrapy projects in SPIDER_DIRS setting
    imported_settings = sys.modules.pop("settings", None)
    for spiders_dir in settings.SPIDER_DIRS:
        for (root, dirshere, fileshere) in os.walk(spiders_dir):
            try:
                fp, pathname, description = imp.find_module("settings", [root + os.sep])
            except ImportError:
                continue
            if fp is not None:
                try:
                    spider_settings = imp.load_module("settings", fp, pathname, description)
                    if hasattr(spider_settings, "SPIDER_MODULES"):
                        SpiderProject.objects.create(path=os.path.dirname(os.path.dirname(pathname)))
                    sys.modules.pop("settings")
                except ImportError:
                    pass
                finally:
                    fp.close()
    if imported_settings is not None:
        # is this how you re-import a module?
        sys.modules["settings"] = imported_settings


def enumerate_spider_classes():
    original_cd = os.getcwd()
    imported_settings = sys.modules.pop("settings", None)
    for spider_project in SpiderProject.objects.all():
        os.chdir(spider_project.path)
        os.environ.pop(ENVVAR, None)  # force get_project_settings() to reconsider the current directory
        project_settings = get_project_settings()
        for module_or_package_name in project_settings.get("SPIDER_MODULES"):
            for module in walk_modules(module_or_package_name):
                for spider_cls in iter_spider_classes(module):
                    yield (spider_project, spider_cls)
    if imported_settings is not None:
        sys.modules["settings"] = imported_settings
    os.chdir(original_cd)
