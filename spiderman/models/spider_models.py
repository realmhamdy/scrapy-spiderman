from django.db import models
from app_models import BaseItem


"""
[[[cog
from scrapy.item import Item, Field
import warnings
import six
import cog
from spiderman.util import enumerate_spider_classes


cog.outl()
cog.outl()


for spider_project, spider_cls in enumerate_spider_classes():
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
            cog.outl('    file = models.FileField(upload_to="spiderfiles/{}/files/%Y/%m/%d/%H/%M/%S")'.format(spider_cls.__name__))
        elif field_name == "image_urls":
            cog.outl('    image = models.ImageField(upload_to="spiderfiles/{}/images/%Y/%m/%d/%H/%M/%S")'.format(spider_cls.__name__))
        else:
            cog.outl("    %s = models.CharField(max_length=255, null=True, blank=True)" % field_name)
    cog.outl()
    cog.outl("    class Meta:")
    cog.outl("        app_label = 'spiderman'")
    cog.outl()
    cog.outl()
]]]"""


#[[[end]]]