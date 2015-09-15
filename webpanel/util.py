import imp
from os import walk as walk_dir
import os
import os.path as pth
import sys
from imp import reload
from importlib import import_module
from django.conf import settings
from django import setup
from django.core.management.commands.makemigrations import Command as MakeMigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
from cogapp import Cog
from . import models
from .models import spider_models


def start_django(**options):
    # this can be used from scripts that need Django functionality
    if not settings.configured:
        settings.configure(**options)
        setup()


def generate_models():
    target_file = pth.join(pth.dirname(__file__), "models", "spider_models.py")
    Cog().main([sys.argv[0], "-r", target_file])
    reload(spider_models)
    reload(models)
    MakeMigrationsCommand().run_from_argv([sys.argv[0], "makemigrations"])
    MigrateCommand().run_from_argv([sys.argv[0], "migrate", "webpanel"])


def erase_models():
    target_file = pth.join(pth.dirname(__file__), "models", "spider_models.py")
    Cog().main([sys.argv[0], "-x", target_file])


def find_spiders():
    # return paths to all spiders' settings modules
    settings_paths = []
    imported_settings = sys.modules.pop("settings", None)
    for spiders_dir in settings.SPIDER_DIRS:
        for (root, dirshere, fileshere) in walk_dir(spiders_dir):
            try:
                fp, pathname, description = imp.find_module("settings", [root + os.sep])
            except ImportError:
                continue
            if fp is not None:
                try:
                    spider_settings = imp.load_module("settings", fp, pathname, description)
                    if hasattr(spider_settings, "SPIDER_MODULES"):
                        settings_paths.append(os.path.dirname(pathname))
                    sys.modules.pop("settings")
                except ImportError:
                    pass
                finally:
                    fp.close()
    if imported_settings is not None:
        # is this how you re-import a module?
        sys.modules["settings"] = imported_settings
    return settings_paths


def enumerate_spider_classes():
    for settings_dir in find_spiders():
        sys.path.insert(0, settings_dir)
        spider_settings = import_module("settings")
        for module_or_package_name in spider_settings.SPIDER_MODULES:
            sys.path.insert(0, pth.normpath(pth.join(settings_dir, pth.pardir)))
            for module in walk_modules(module_or_package_name):
                for spider_cls in iter_spider_classes(module):
                    yield spider_cls
            sys.path.pop(0)
        sys.path.pop(0)
        sys.modules.pop("settings")
