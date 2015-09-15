from django.conf import settings
from django import setup
from django.core.management.commands.makemigrations import Command as MakeMigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
import os.path as pth
import sys
from imp import reload
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
    Cog().main([sys.argv[0], "-d", target_file])
