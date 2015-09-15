from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils import timesince, timezone


class Spider(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    item_model_name = models.CharField(max_length=128, blank=False, null=False,
                                       help_text=_("Used to refer to the item model for this spider"))

    class Meta:
        app_label = "webpanel"

    @property
    def item_model(self):
        return ContentType.objects.get_by_natural_key("webpanel", self.item_model_name).model_class()

    def run(self):
        pass

    def stop(self):
        pass

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Spider {}>".format(self.name)


class SpiderRun(models.Model):

    FINISH_REASON_FAILED = "FL"
    FINISH_REASON_FINISHED = "FN"
    FINISH_REASON_STOPPED = "FSTP"

    FINISH_CHOICES = (
        (FINISH_REASON_FAILED, "Failed"),
        (FINISH_REASON_FINISHED, "Finished"),
        (FINISH_REASON_STOPPED, "Stopped")
    )

    spider = models.ForeignKey(Spider, related_name="runs")
    start_time = models.DateTimeField(auto_now=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    finish_reason = models.CharField(choices=FINISH_CHOICES, max_length=32)
    logfile = models.FileField(upload_to="appdata/logs")

    @property
    def finished(self):
        return self.finish_time is not None

    @property
    def runtime(self):
        return timesince(self.start_time, timezone.now() if self.finish_time is None else self.finish_time)

    def save(self, *args, **kwargs):
        assert self.finish_time is None or \
               self.finish_time > self.start_time, "You've got a nice time machine, still this won't pass"
        return super(SpiderRun, self).save(*args, **kwargs)

    class Meta:
        ordering = ("start_time",)
        app_label = "webpanel"

    def __unicode__(self):
        datetime_fmt = "%d-%m-%Y %H:%M:%S %p"
        return "{} running from [{}] {}".format(self.spider.name, self.start_time.strftime(datetime_fmt),
                                                ", finished at {}".format(self.finish_time.strftime(datetime_fmt))
                                                if self.finished else "[Still running...]")


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
