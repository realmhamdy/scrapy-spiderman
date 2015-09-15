from django.db import models
from app_models import BaseItem


"""
[[[cog
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
from scrapy.item import Item, Field
from importlib import import_module
import sys
import os.path as pth
import warnings
import six
import cog
from webpanel.spider_finder import find_spiders


cog.outl()
cog.outl()

for settings_dir in find_spiders():
    sys.path.insert(0, settings_dir)
    settings = import_module("settings")
    for module_or_package_name in settings.SPIDER_MODULES:
        sys.path.insert(0, pth.normpath(pth.join(settings_dir, pth.pardir)))
        for module in walk_modules(module_or_package_name):
            for spider_cls in iter_spider_classes(module):
                if not hasattr(spider_cls, "ITEM_CLASS") or \
                    not issubclass(getattr(spider_cls, "ITEM_CLASS"), Item):
                    warnings.warn(("{0} spider doesn't have the required attribute ITEM_CLASS. " +\
                        "Ignoring {0}").format(spider_cls.__name__))
                    continue
                ITEM_CLASS = spider_cls.ITEM_CLASS
                cog.outl("class %s(BaseItem):" % (ITEM_CLASS.__name__,))
                cog.outl()
                for (field_name, field_value) in six.iteritems(ITEM_CLASS.fields):
                    assert isinstance(field_value, Field), "Found non-field in item '%s' fields" % ITEM_CLASS.__name__
                    if field_name in ("files", "images"): continue
                    if field_name == "file_urls":
                        cog.outl('    file = models.FileField(upload_to="spiderfiles/%s/files")' % (spider_cls.__name__,))
                    elif field_name == "image_urls":
                        cog.outl('    image = models.ImageField(upload_to="spiderfiles/%s/images")' % (spider_cls.__name__,))
                    else:
                        cog.outl("    %s = models.CharField(max_length=255, null=True, blank=True)" % field_name)
                cog.outl()
                cog.outl("    class Meta:")
                cog.outl("        app_label = 'webpanel'")
                cog.outl()
                cog.outl()
        sys.path.pop(0)
    sys.path.pop(0)
    sys.modules.pop("settings")
]]]"""

#[[[end]]]