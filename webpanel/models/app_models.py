from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class Spider(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    running = models.BooleanField(default=False)
    runtime = models.DateTimeField(null=True, blank=True, help_text=_("The last time this spider was started"))
    item_model_name = models.CharField(max_length=128, blank=False, null=False,
                                       help_text=_("Used to refer to the item model for this spider"))

    class Meta:
        app_label = "webpanel"

    @property
    def item_model(self):
        return ContentType.objects.get_by_natural_key("webpanel", self.item_model_name).model_class()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Spider {}>".format(self.name)


class BaseItem(models.Model):

    # %(class)s stands for subclass name
    spider = models.ForeignKey(Spider, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        app_label = "webpanel"
        abstract = True

    def __unicode__(self):
        return "Item for spider '{}'".format(self.spider.name)

    def __repr__(self):
        return "<BaseItem, spider={}>".format(self.spider.name)
