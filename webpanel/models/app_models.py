from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Spider(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    running = models.BooleanField(default=False)
    runtime = models.DateTimeField(null=True, blank=True, help_text=_("The last time this spider was started"))

    class Meta:
        app_label = "webpanel"

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
