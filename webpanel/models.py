from django.db import models


class Spider(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    running = models.BooleanField(default=False, null=True, blank=True)
    runtime = models.DateTimeField(null=True, blank=True)
